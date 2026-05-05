from pydantic import BaseModel
from typing import Optional

class CategoryOut(BaseModel):
    id: int
    name: str
    complete_name: Optional[str] = None
    parent_id: Optional[int] = None
    parent_name: Optional[str] = None