from typing import Dict, Any
from app.infrastructure.database.database_adapter import async_get_product_from_db
from app.infrastructure.kafka.producer import send_to_kafka
from app.adapters.vendor_adapter import fetch_product_data


async def get_product_by_id(product_id: str) -> Dict[str, Any]:
    """
    Belirli bir ürünü getir. Eğer ürün bulunamazsa vendor'dan çek ve Kafka'ya gönder.

    Args:
        product_id (str): Ürünün benzersiz kimliği.

    Returns:
        Dict[str, Any]: Ürün bilgisi, hata mesajı veya işlem durumu.
    """
    try:
        # Veritabanından ürünü al
        product = await async_get_product_from_db(product_id)
        if product:
            return {"data": product}

        # Ürün verisi vendor'dan alınmaya çalışılıyor
        product_data = await fetch_product_data(product_id)
        if not product_data:
            return {"error": "Product not found"}

        # Ürün Kafka'ya gönderiliyor
        await send_to_kafka(product_data)
        return {"message": "Data is being processed. Please try again later."}

    except Exception as e:
        # Beklenmeyen hataları yakala ve bildir
        return {"error": f"An error occurred: {str(e)}"}
