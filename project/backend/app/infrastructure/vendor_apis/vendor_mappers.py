from app.domain.models import Product

def map_vendor_data_to_product(vendor_data: dict) -> Product:
    """
    Vendor verisini `Product` domain modeline dönüştür.
    """
    return Product(
        id=vendor_data.get("id"),
        name=vendor_data.get("name"),
        description=vendor_data.get("description", ""),
        price=vendor_data.get("price", 0.0),
        photos=vendor_data.get("photos", []),
    )
