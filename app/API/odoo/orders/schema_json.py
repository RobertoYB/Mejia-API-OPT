from pydantic import BaseModel

class Order(BaseModel):
    id: int
    name: str
    date_order: str
    company_id: int | None = None
    company_name: str | None = None
    partner_id: int | None = None
    partner_name: str | None = None
    amount_total: float
    state: str