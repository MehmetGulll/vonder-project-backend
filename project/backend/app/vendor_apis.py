import httpx


MOCK_DATA = {
    "vendor1": [
        {"ProductName": "Vendor1 Product 1", "ProductDescription": "Vendor1 Product 1 Description", "ProductPrice": 29.99},
        {"ProductName": "Vendor1 Product 2", "ProductDescription": "Vendor1 Product 2 Description", "ProductPrice": 19.99}
    ],
    "vendor2": [
        {"Product_Name": "Vendor2 Product 1", "Product_Description": "Vendor2 Product 1 Description", "Product_Price": 39.99},
        {"Product_Name": "Vendor2 Product 2", "Product_Description": "Vendor2 Product 2 Description", "Product_Price": 24.99}
    ]
}


field_mapping = {
    "ProductName": "name",
    "Product_Name": "name",
    "ProductDescription": "description",
    "Product_Description": "description",
    "ProductPrice": "price",
    "Product_Price": "price",
    "ProductPhotos": "photos",
    "Product_Photos": "photos",
}

def map_vendor_data_to_standard(vendor_data, field_mapping):
    """
    Vendor verilerini standart modele dönüştür.
    """
    standardized_data = {}
    for vendor_field, value in vendor_data.items():
        # Eşlemeye göre standart alan adı belirle
        standard_field = field_mapping.get(vendor_field, vendor_field)  # Eşleme yoksa orijinal alan kullanılır
        standardized_data[standard_field] = value
    return standardized_data


async def get_product_from_vendor(vendor_name: str, product_id: str):
    """
    Belirtilen vendor'dan ürün bilgisini al.
    """
    for product in MOCK_DATA.get(vendor_name, []):
        if product.get("ProductName") == f"Vendor1 Product {product_id}" or \
           product.get("Product_Name") == f"Vendor2 Product {product_id}":
            # Vendor verisini standart modele dönüştür
            return map_vendor_data_to_standard(product, field_mapping)

    raise Exception(f"Product {product_id} not found for vendor {vendor_name}")


def get_all_vendors_and_product_ids():
    """
    MOCK_DATA'dan tüm vendor ve ürün ID'lerini dinamik olarak al.
    """
    vendors = MOCK_DATA.keys()
    product_ids = set()
    for vendor_products in MOCK_DATA.values():
        for product in vendor_products:
            # Hem "ProductName" hem de "Product_Name" alanından ID'yi tahmin et
            product_id = product.get("ProductName", product.get("Product_Name", "")).split(" ")[-1]
            product_ids.add(product_id)
    return list(vendors), list(product_ids)
