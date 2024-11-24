from typing import Dict, Any
from app.infrastructure.database.database_adapter import async_get_all_products


async def get_all_products(limit: int, offset: int) -> Dict[str, Any]:
    """
    Tüm ürünleri al ve vendor bazında gruplandır.

    Args:
        limit (int): Döndürülecek ürünlerin maksimum sayısı.
        offset (int): Atlanacak ürünlerin sayısı.

    Returns:
        Dict[str, Any]: Gruplandırılmış ürünlerin listesi veya mesaj içeren bir sözlük.
    """
    try:
        # Veritabanından ürünleri al
        products = await async_get_all_products(limit, offset)
        if not products:
            return {"message": "No products found"}

        # Ürünleri vendor bazında gruplandır
        grouped_products = {}
        for product in products:
            vendor_name = product["id"].split("-")[0]
            grouped_products.setdefault(vendor_name, []).append(product)

        return {"data": grouped_products}

    except Exception as e:
        # Hata durumunda uygun bir mesaj döndür
        return {"error": f"Error fetching products: {str(e)}"}
