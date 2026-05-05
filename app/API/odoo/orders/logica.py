from app.Core.odoo_client import models, uid
from app.Core.config import settings
from app.API.odoo.orders.schema_json import Order

def get_orders():
    orders = models.execute_kw(
        settings.ODOO_DB,
        uid,
        settings.ODOO_PASSWORD,
        'sale.order',
        'search_read',
        [[]],
        {'fields': ['id', 'name', 'date_order', 'company_id', 'partner_id', 'amount_total', 'state']}
    )

    #El company_id y el partner_id son un many2one, entonces se tienen que separar.
    correct_orders = []
    for item in orders:
        correct_orders.append(Order(
        id = item['id'],
        name = item['name'],
        date_order = item['date_order'],
        company_id = item['company_id'][0] if item['company_id'] else None,  #Checa si tiene un valor, si no tiene entonces le pone None
        company_name = item['company_id'][1] if item['company_id'] else None,
        partner_id = item['partner_id'][0] if item['partner_id'] else None,
        partner_name = item['partner_id'][1] if item['partner_id'] else None,
        amount_total = item['amount_total'],
        state = item['state']
    ))
        
    return correct_orders