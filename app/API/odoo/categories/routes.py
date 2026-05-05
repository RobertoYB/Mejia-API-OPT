from fastapi import APIRouter
from .logica import get_categories
from .schema_json import CategoryOut

router = APIRouter()

@router.get("/", response_model=list[CategoryOut])
def read_categories():
    return get_categories()