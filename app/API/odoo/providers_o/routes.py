from fastapi import APIRouter
from app.API.odoo.providers_o.schema_json import Provider
from app.API.odoo.providers_o.logica import get_providers
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Provider])
def list_providers():
    return get_providers()

