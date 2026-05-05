from pydantic import BaseModel

class StockProduct(BaseModel):
    id: int
    name: str
    default_code: str | None = None
    qty_available: float
