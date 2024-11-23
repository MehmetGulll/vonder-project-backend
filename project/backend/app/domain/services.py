from .models import Product
from .repositories import ProductRepository
from typing import List

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_all_products(self, limit: int, offset: int) -> List[Product]:
        return await self.repository.get_all_products(limit, offset)

    async def get_product_by_id(self, product_id: str) -> Product:
        return await self.repository.get_product_by_id(product_id)

    async def save_product(self, product: Product) -> None:
        await self.repository.save_product(product)
