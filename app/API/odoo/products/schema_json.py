from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    list_price: float
    default_code: Optional[str] = None
