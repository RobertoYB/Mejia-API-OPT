from pydantic import BaseModel
from typing import Optional


class CustomerOut(BaseModel):
    id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
