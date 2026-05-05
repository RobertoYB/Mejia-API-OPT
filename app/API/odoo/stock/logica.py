from app.Core.odoo_client import models, uid
from app.Core.config import settings

def get_stock_products():
    products = models.execute_kw(
        settings.ODOO_DB,
        uid,
        settings.ODOO_PASSWORD,
        'product.product',
        'search_read',
        [[]],  # sin filtros, trae todos
        {
            'fields': [
                'id',
                'name',
                'default_code',
                'qty_available'
            ]
        }
    )

    for p in products:
        p["default_code"] = p.get("default_code") or None

    return products
