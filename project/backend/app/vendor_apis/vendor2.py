import httpx

async def get_product(product_id: str):
    # Vendor4 API çağrısı
    # Örnek response
    return {
        "id": product_id,
        "name": "Sample Product from Vendor4",
        "description": "This is a sample description from Vendor4",
        "price": 19.99,
        "photos": ["https://parsadi.com/wp-content/uploads/2022/12/Vendor.jpg"],
    }
