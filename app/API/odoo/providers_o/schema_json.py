from pydantic import BaseModel

class Provider(BaseModel):
    id: int
    name: str
    email: str | None = None
    phone: str | None = None