from fastapi import APIRouter
from typing import List
from app.API.odoo.stock.logica import get_stock_products
from app.API.odoo.stock.schema_json import StockProduct

router = APIRouter()

@router.get("/", response_model=List[StockProduct])
def list_stock():
    return get_stock_products()
