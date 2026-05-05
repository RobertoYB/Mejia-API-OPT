from fastapi import APIRouter
from app.Core.prestashop_client import prestashop_get
from app.API.prestashop.utils import ps_success, ps_error

router = APIRouter()

fieldspayments = "id,order_reference,amount,payment_method,transaction_id,date_add"

@router.get("/")
def get_payments():
    try:
        data = prestashop_get("order_payments", fieldspayments)

        if not data:
            return ps_error("404", "No se encontraron pagos")
        
        return ps_success(data)

    except Exception as e:
        return ps_error("500", str(e))
