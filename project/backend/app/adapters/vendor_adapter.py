from typing import Tuple, List
from app.core.mock_data import MOCK_DATA
from app.core.mappers import map_vendor_data_to_standard, field_mapping


async def get_product_from_vendor(vendor_name: str, product_id: str):
    """
    Belirtilen vendor'dan ürün bilgisini al.
    """
    vendor_products = MOCK_DATA.get(vendor_name, [])
    if not vendor_products:
        print(f"No products found for vendor {vendor_name}")
        raise Exception(f"No products found for vendor {vendor_name}")

    for product in vendor_products:
        print(f"Checking product: {product} for product_id: {product_id}")


        if (
            product.get("id") == product_id or
            product.get("ProductID") == product_id or
            product.get("Product_Id") == product_id
        ):
            print(f"Found matching product: {product}")

            vendor_data = {**product, "vendor_name": vendor_name, "product_id": product_id}
            return map_vendor_data_to_standard(vendor_data, field_mapping)

        if (
            product.get("ProductName", "").endswith(f"Product {product_id}") or
            product.get("Product_Name", "").endswith(f"Product {product_id}")
        ):
            print(f"Found matching product by name: {product}")

            vendor_data = {**product, "vendor_name": vendor_name, "product_id": product_id}
            return map_vendor_data_to_standard(vendor_data, field_mapping)

    print(f"No matching product found for product_id: {product_id} in vendor: {vendor_name}")
    raise Exception(f"Product {product_id} not found for vendor {vendor_name}")






def get_all_vendors_and_product_ids() -> Tuple[List[str], List[str]]:
    """
    MOCK_DATA'dan tüm vendor ve ürün ID'lerini al.
    
    Returns:
        Tuple[List[str], List[str]]: Vendor isimleri ve ürün ID'lerinden oluşan bir tuple.
    """
    vendors = MOCK_DATA.keys()
    product_ids = set()
    for vendor_products in MOCK_DATA.values():
        for product in vendor_products:
            product_id = product.get("ProductName", product.get("Product_Name", "")).split(" ")[-1]
            product_ids.add(product_id)
    return list(vendors), list(product_ids)
