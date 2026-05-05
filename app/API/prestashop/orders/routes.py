from fastapi import APIRouter
from app.Core.prestashop_client import prestashop_get
from app.API.prestashop.utils  import ps_error, ps_success

router = APIRouter()

fieldsorders = "id,id_customer,total_paid,date_add,reference"

@router.get("/")
def get_products():
    try:
        data = prestashop_get("orders", fieldsorders)

        if not data:
            return ps_error("404", "No se encontraron ordenes")
        
        return ps_success(data)
    
    except Exception as e:
        return ps_error("500",str(e) )
    
@router.get("/ref/{reference}")
def get_orders_ref(reference: str):
    try:
        data = prestashop_get("orders", fieldsorders, filters={"reference": reference})

        if not data:
            return ps_error("404", "No se encontró una orden con la referencia dada")
        
        return ps_success(data)
    
    except Exception as e:
        return ps_error("500",str(e) )
        

        