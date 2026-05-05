from pydantic import BaseModel
from typing import Optional


class ProductUpdate(BaseModel):
    price: Optional[float] = None
    wholesale_price: Optional[float] = None
    active: Optional[int] = None
    available_for_order: Optional[int] = None
    show_price: Optional[int] = None
    online_only: Optional[int] = None
    minimal_quantity: Optional[int] = None
    additional_shipping_cost: Optional[float] = None
    unity: Optional[str] = None
    unit_price: Optional[float] = None
    unit_price_ratio: Optional[float] = None
    reference: Optional[str] = None
    supplier_reference: Optional[str] = None
    location: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    depth: Optional[float] = None
    weight: Optional[float] = None
    condition: Optional[str] = None
    redirect_type: Optional[str] = None
    id_type_redirected: Optional[int] = None
    available_date: Optional[str] = None
    visibility: Optional[str] = None
    state: Optional[int] = None