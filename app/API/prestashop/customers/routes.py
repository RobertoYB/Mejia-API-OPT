from fastapi import APIRouter
from app.Core.prestashop_client import prestashop_get
from app.API.prestashop.utils import ps_success, ps_error

router = APIRouter()

# Campos que vamos a pedirle a PrestaShop
fields = "id,email,firstname,lastname,date_add,active"

@router.get("/")
def get_customers():
    try:
        data = prestashop_get("customers", fields)

        if not data:
            return ps_error("404", "No se encontraron clientes")

        return ps_success(data)

    except Exception as e:
        return ps_error("500", str(e))