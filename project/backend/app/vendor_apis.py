import httpx

MOCK_DATA = {
    "vendor1": [
        {"id": "1", "name": "Vendor1 Product 1", "description": "Vendor1 Product 1 Description", "price": 29.99},
        {"id": "2", "name": "Vendor1 Product 2", "description": "Vendor1 Product 2 Description", "price": 19.99}
    ],
    "vendor2": [
        {"id": "1", "name": "Vendor2 Product 1", "description": "Vendor2 Product 1 Description", "price": 39.99},
        {"id": "2", "name": "Vendor2 Product 2", "description": "Vendor2 Product 2 Description", "price": 24.99}
    ]
}


async def get_product_from_vendor(vendor_name: str, product_id: str):

    for product in MOCK_DATA.get(vendor_name, []):
        if product["id"] == product_id:
            return product
    raise Exception(f"Product {product_id} not found for vendor {vendor_name}")

def get_all_vendors_and_product_ids():
    """
    MOCK_DATA'dan tüm vendor ve ürün ID'lerini dinamik olarak al.
    """
    vendors = MOCK_DATA.keys()
    product_ids = set()
    for vendor_products in MOCK_DATA.values():
        for product in vendor_products:
            product_ids.add(product["id"])
    return list(vendors), list(product_ids)

