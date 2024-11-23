from app.domain.models import Product

# Vendor alanlarını normalize eden eşleme tablosu
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

def normalize_vendor_data(vendor_data: dict) -> dict:
    """
    Vendor verisini normalize eder.
    """
    normalized_data = {}
    for vendor_field, value in vendor_data.items():

        standard_field = field_mapping.get(vendor_field, vendor_field)
        normalized_data[standard_field] = value
    return normalized_data

def map_vendor_data_to_product(vendor_data: dict) -> Product:
    """
    Vendor verisini `Product` domain modeline dönüştür.
    """

    normalized_data = normalize_vendor_data(vendor_data)


    return Product(
        id=normalized_data.get("id"),
        name=normalized_data.get("name"),
        description=normalized_data.get("description", ""),
        price=normalized_data.get("price", 0.0),
        photos=normalized_data.get("photos", []),
    )
