from pydantic import BaseModel
from typing import List, Optional


class Pet(BaseModel):
    id: Optional[int] = None
    name: str
    photoUrls: List[str]
    status: Optional[str] = None


class Order(BaseModel):
    id: Optional[int] = None
    petId: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[str] = None
    complete: Optional[bool] = None