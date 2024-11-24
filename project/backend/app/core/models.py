from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    photos: List[str]
