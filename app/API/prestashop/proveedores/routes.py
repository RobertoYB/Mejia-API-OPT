from fastapi import APIRouter
from app.Core.prestashop_client import prestashop_get
from app.API.prestashop.utils import ps_success, ps_error

router = APIRouter()

fieldssuppliers = "id,name,active,date_add,date_upd"

@router.get("/")
def get_suppliers():
    try:
        data = prestashop_get("suppliers", fieldssuppliers)

        if not data:
            return ps_error("404", "No se encontraron proveedores")
        
        return ps_success(data)

    except Exception as e:
        return ps_error("500", str(e))