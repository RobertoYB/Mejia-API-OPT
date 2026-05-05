from fastapi import APIRouter, HTTPException
from app.Core.odoo_client import models, uid
from app.Core.woocommerce_client import wcapi
from app.Core.config import settings

router = APIRouter()

@router.get("/")
def get_orders(per_page: int = 10):
    try:
        response = wcapi.get("orders", params={"per_page": per_page})

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        orders = response.json()

        clean_orders = []

        for order in orders:
            clean_orders.append({
                "id": order["id"],
                "status": order["status"],
                "total": order["total"],
                "currency": order["currency"],
                "date_created": order["date_created"],
                "customer_id": order["customer_id"],
                "created_via": order["created_via"],
                "products": [
                    {
                        "name": item["name"],
                        "quantity": item["quantity"],
                        "price": item["price"]
                    }
                    for item in order["line_items"]
                ]
            })

        return clean_orders

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/create-order")
def create_orders():
    orders = models.execute_kw(
        settings.ODOO_DB,
        uid,
        settings.ODOO_PASSWORD,
        'sale.order',
        'search_read',
        [[]],
        {'fields': ['id', 'name']}
    )

    created = []
    skipped = []

    existing_response = wcapi.get("orders", params={"per_page": 100})

    existing_odoo_orders = set()

    if existing_response.status_code == 200:
        existing_orders = existing_response.json()

        for o in existing_orders:
            for meta in o.get("meta_data", []):
                if meta["key"] == "odoo_order":
                    existing_odoo_orders.add(meta["value"])

    for order in orders:

        if order['name'] in existing_odoo_orders:
            print(f"Orden ya existe: {order['name']}")
            skipped.append(order['name'])
            continue

        lines = models.execute_kw(
            settings.ODOO_DB,
            uid,
            settings.ODOO_PASSWORD,
            'sale.order.line',
            'search_read',
            [[['order_id', '=', order['id']]]],
            {'fields': ['product_id', 'product_uom_qty']}
        )

        line_items = []

        for line in lines:
            product_id_odoo = line['product_id'][0]
            qty = int(line['product_uom_qty'])

            product_data = models.execute_kw(
                settings.ODOO_DB,
                uid,
                settings.ODOO_PASSWORD,
                'product.product',
                'read',
                [[product_id_odoo]],
                {'fields': ['default_code']}
            )

            if not product_data or not product_data[0].get('default_code'):
                print(f"Producto sin SKU en Odoo: {line['product_id'][1]}")
                continue

            sku = product_data[0]['default_code']

            response = wcapi.get("products", params={"sku": sku})

            if response.status_code != 200:
                print(f"Error Woo buscando SKU: {sku}")
                continue

            products = response.json()

            if not products:
                print(f"Producto NO existe en Woo: {sku}")
                continue

            product_id_wc = products[0]['id']

            line_items.append({
                "product_id": product_id_wc,
                "quantity": qty
            })

        if not line_items:
            print(f"Orden {order['name']} sin productos válidos")
            continue

        data = {
            "payment_method": "cod",
            "set_paid": True,
            "line_items": line_items,
            "meta_data": [
                {
                    "key": "odoo_order",
                    "value": order['name']
                }
            ]
        }

        response = wcapi.post("orders", data)

        print(f"ORDER: {order['name']}")
        print(f"STATUS: {response.status_code}")
        print(f"RESPONSE: {response.json()}")

        if response.status_code == 201:
            created.append(order['name'])

    return {
        "created": created,
        "skipped": skipped
    }