import xmlrpc.client
from app.Core.config import settings

common = xmlrpc.client.ServerProxy(f"{settings.ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(
    settings.ODOO_DB,
    settings.ODOO_USER,
    settings.ODOO_PASSWORD,
    {}
)

models = xmlrpc.client.ServerProxy(
    f"{settings.ODOO_URL}/xmlrpc/2/object"
)