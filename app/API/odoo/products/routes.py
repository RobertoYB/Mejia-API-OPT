from fastapi import APIRouter
from app.API.odoo.products.schema_json import Product
from typing import List
from app.Core.odoo_client import models, uid
from app.Core.config import settings

router = APIRouter()

@router.get("/", response_model=List[Product])
def get_products():
    products = models.execute_kw(
        settings.ODOO_DB,
        uid,
        settings.ODOO_PASSWORD,
        'product.template',
        'search_read',
        [[]],
        {'fields': ['id', 'name', 'list_price', 'default_code'], 'limit': 100}
    )

    for p in products:
        if p.get("default_code") is False:
            p["default_code"] = None

    return products