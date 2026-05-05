from fastapi import APIRouter
from app.API.odoo.orders.schema_json import Order
from app.API.odoo.orders.logica import get_orders
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Order])
def list_orders():
    return get_orders()