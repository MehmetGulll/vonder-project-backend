from fastapi import FastAPI, Query
from threading import Thread
from app.infrastructure.database.tables import create_products_table
from app.application.use_cases.sync_products import fetch_and_save_initial_products
from app.application.services.kafka_consumer import start_kafka_consumer
from app.application.use_cases.get_all_products import get_all_products

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Veritabanı tablolarını oluştur
    await create_products_table()

    # Kafka tüketici başlat
    kafka_thread = Thread(target=start_kafka_consumer)
    kafka_thread.start()

    # MOCK_DATA ile veritabanını doldur
    await fetch_and_save_initial_products()

@app.get("/health")
async def health_check():
    """
    Sağlık kontrolü endpoint'i.
    """
    return {"status": "ok"}

@app.get("/products")
async def products_endpoint(
    limit: int = Query(10, description="Kaç ürün döndürülecek"),
    offset: int = Query(0, description="Kaç ürün atlanacak")
):
    """
    Tüm ürünleri listeleyen endpoint.
    """
    try:
        products = await get_all_products(limit, offset)
        return products
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
