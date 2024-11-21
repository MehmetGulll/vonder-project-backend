import httpx

async def get_product(product_id: str):
    url = f"https:api.vendor3.com/products/{product_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code ==200:
            return response.json()
        return None