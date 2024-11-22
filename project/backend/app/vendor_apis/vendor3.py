
async def get_product(product_id: str):
    return {
        "id": product_id,
        "name": "Vendor3",
        "description": "Vendor3 desc",
        "price": 19.99,
        "photos": ["https://parsadi.com/wp-content/uploads/2022/12/Vendor.jpg"],
    }
