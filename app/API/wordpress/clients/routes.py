from fastapi import APIRouter, HTTPException
from app.Core.odoo_client import models, uid
from app.Core.woocommerce_client import wcapi
from app.Core.config import settings

router = APIRouter()

@router.post("/create-client")
def create_clients():
    clients = models.execute_kw(
        settings.ODOO_DB,
        uid,
        settings.ODOO_PASSWORD,
        'res.partner',
        'search_read',
        [[['customer_rank', '>', 0]]],
        {'fields': ['id', 'name', 'email', 'phone']}
    )

    created = []
    skipped = []

    existing_response = wcapi.get("customers", params={"per_page": 100})

    existing_odoo_clients = set()

    if existing_response.status_code == 200:
        existing_clients = existing_response.json()

        for o in existing_clients:
            for meta in o.get("meta_data", []):
                if meta["key"] == "odoo_partner":
                    existing_odoo_clients.add(meta["value"])

    for client in clients:

        if client['name'] in existing_odoo_clients:
            print(f"El cliente ya existe: {client['name']}")
            skipped.append(client['name'])
            continue

        data = {
            "first_name": client['name'],
            "email": client['email'],
            "billing": {
                "phone": client['phone']
            },
            "meta_data": [
                {
                    "key": "odoo_partner",
                    "value": client['name']
                }
            ]
        }

        response = wcapi.post("customers", data)

        print(f"client: {client['name']}")
        print(f"STATUS: {response.status_code}")
        print(f"RESPONSE: {response.json()}")

        if response.status_code == 201:
            created.append(client['name'])

    return {
        "created": created,
        "skipped": skipped
    }