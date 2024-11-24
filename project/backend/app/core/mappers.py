field_mapping = {
    "ProductName": "name",
    "Product_Name": "name",
    "ProductDescription": "description",
    "Product_Description": "description",
    "ProductPrice": "price",
    "Product_Price": "price",
    "ProductPhotos": "photos",
    "Product_Photos": "photos",
    "ProductID": "id",  
    "Product_Id": "id", 
}


def map_vendor_data_to_standard(vendor_data: dict, field_mapping: dict) -> dict:

    standardized_data = {}
    for vendor_field, value in vendor_data.items():
  
        standard_field = field_mapping.get(vendor_field, vendor_field)
        standardized_data[standard_field] = value


    if "id" not in standardized_data or not standardized_data["id"]:
        standardized_data["id"] = f"{vendor_data.get('vendor_name', 'unknown')}-{vendor_data.get('product_id', 'unknown')}"

    return standardized_data
