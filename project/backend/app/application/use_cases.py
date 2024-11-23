from app.domain.services import ProductService
from app.domain.models import Product

class GetAllProductsUseCase:
    def __init__(self, service: ProductService):
        self.service = service

    async def execute(self, limit: int, offset: int):
        return await self.service.get_all_products(limit, offset)

class SaveProductUseCase:
    def __init__(self, service: ProductService):
        self.service = service

    async def execute(self, product: Product):
        await self.service.save_product(product)
