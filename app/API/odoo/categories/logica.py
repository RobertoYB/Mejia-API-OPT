from app.Core.odoo_client import models, uid
from app.Core.config import settings

def get_categories():
    categories = models.execute_kw(
        settings.ODOO_DB,
        uid,
        settings.ODOO_PASSWORD,
        "product.category",
        "search_read",
        [[]],
        {"fields": ["id", "name", "complete_name", "parent_id"]}
    )

    for c in categories:
        parent = c.get("parent_id")
        if parent:
            c["parent_id"] = parent[0]
            c["parent_name"] = parent[1]
        else:
            c["parent_id"] = None
            c["parent_name"] = None

    return categories