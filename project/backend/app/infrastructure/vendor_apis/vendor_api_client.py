import httpx
from typing import Dict, Any, List
from app.infrastructure.vendor_mappers import map_vendor_data_to_product
from app.domain.models import Product

class VendorAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_product(self, product_id: str) -> Product:
        """
        Tek bir ürünü vendor API'den al ve domain modeline dönüştür.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/products/{product_id}")
            response.raise_for_status()
            raw_data = response.json()
            return map_vendor_data_to_product(raw_data)  

    async def get_all_products(self) -> List[Product]:
        """
        Tüm ürünleri vendor API'den al ve domain modeline dönüştür.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/products")
            response.raise_for_status()
            raw_data_list = response.json()
            return [map_vendor_data_to_product(data) for data in raw_data_list]  
