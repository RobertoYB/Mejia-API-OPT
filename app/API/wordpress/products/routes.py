from fastapi import APIRouter
from app.Core.woocommerce_client import wcapi
from app.Core.odoo_client import models, uid
from app.Core.config import settings

router = APIRouter()

@router.get("/create")
def create_products():
    odoo_productos = models.execute_kw(
        settings.ODOO_DB, uid, settings.ODOO_PASSWORD,
        'product.template','search_read',[[]],
        {'fields': ['id','name','list_price','default_code','qty_available']}
    )

    response = wcapi.get("products", params={"per_page": 100})

    existing_refs = set()

    if response.status_code == 200:
        productos_wp = response.json()
        for p in productos_wp:
            sku = p.get("sku")
            if sku:
                existing_refs.add(sku)

    created_products = []
    skipped_products = []
    created = 0
    skipped = 0

    for product in odoo_productos:
        ref = product.get("default_code")  # SKU
        price = product.get("list_price")
        stock = product.get("qty_available")
        name = product.get("name")

        if not ref:
            skipped += 1
            skipped_products.append(name)
            continue

        if ref in existing_refs:
            skipped += 1
            skipped_products.append(name)
            continue

        if price is None or float(price) <= 0:
            skipped += 1
            skipped_products.append(name)
            continue

        if stock is None or float(stock) < 0:
            skipped += 1
            skipped_products.append(name)
            continue


        data = {
            "name": name,
            "type": "simple",
            "regular_price": str(price), 
            "sku": ref,
            "stock_quantity": int(stock),
            "manage_stock": True
        }

        response = wcapi.post("products", data)

        created += 1
        created_products.append(name)
    
    return {
        "Creados": created_products,
        "Saltados": skipped_products,
        "Total creados": created,
        "Total saltados": skipped
    }

@router.get("/")
def get_woocommerce_products():
    response = wcapi.get("products")

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")