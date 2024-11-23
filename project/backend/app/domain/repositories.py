from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Product

class ProductRepository(ABC):
    @abstractmethod
    async def get_all_products(self, limit: int, offset: int) -> List[Product]:
        pass

    @abstractmethod
    async def get_product_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    async def save_product(self, product: Product) -> None:
        pass
