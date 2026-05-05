from app.Core.odoo_client import models, uid
from app.Core.config import settings

def get_providers():
    providers = models.execute_kw(
        settings.ODOO_DB,
        uid,
        settings.ODOO_PASSWORD,
        'res.partner',
        'search_read',
        [[['supplier_rank', '>', 0]]],
        {'fields': ['id', 'name', 'email', 'phone']}
    )

    for p in providers:
        p["email"] = p.get("email") or None
        p["phone"] = p.get("phone") or None

    return providers