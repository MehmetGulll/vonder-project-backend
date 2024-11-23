import httpx
from typing import Dict, Any, List

class VendorAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/products/{product_id}")
            response.raise_for_status()
            return response.json()

    async def get_all_products(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/products")
            response.raise_for_status()
            return response.json()
