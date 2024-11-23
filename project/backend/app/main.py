# from fastapi import FastAPI, HTTPException, Query
# import asyncio
# import random
# import httpx
# from threading import Thread
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# from app.db import (
#     async_get_product_from_db,
#     async_get_all_products,
#     create_products_table,
#     async_save_product_to_db,
# )
# from app.kafka import send_to_kafka, kafka_consumer_thread 
# from app.vendor_apis import (
#     get_product_from_vendor,
#     get_all_vendors_and_product_ids,
#     map_vendor_data_to_standard,
#     field_mapping,
# )

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.on_event("startup")
# async def startup_event():

#     await create_products_table()
#     kafka_thread = Thread(target=kafka_consumer_thread)
#     kafka_thread.start()
#     await fetch_and_save_initial_products()

# @app.get("/health")
# async def health_check():
 
#     return {"status": "ok"}

# @app.get("/products")
# async def get_all_products(
#     limit: int = Query(10, description="Dönen ürün sayısı"),
#     offset: int = Query(0, description="Atlanacak ürün sayısı"),
# ):
  
#     products = await async_get_all_products(limit, offset)
#     if not products:
#         return {"message": "No products found"}

#     normalized_products = []
#     for product in products:

#         if "-" not in product["id"]:
#             product["id"] = f"vendor4-{product['id']}"  
#         normalized_products.append(product)


#     grouped_products = {}
#     for product in normalized_products:
#         vendor_name = product["id"].split("-")[0]
#         grouped_products.setdefault(vendor_name, []).append(product)

#     return {"data": grouped_products}

# @app.get("/products")
# async def get_all_products(
#     limit: int = Query(10, description="Dönen ürün sayısı"),
#     offset: int = Query(0, description="Atlanacak ürün sayısı"),
# ):
#     products = await async_get_all_products(limit, offset)
#     if not products:
#         return {"message": "No products found"}

#     grouped_products = {}
#     for product in products:
#         print(f"[DEBUG] ID before grouping: {product['id']}")  # Endpoint içinde ID'yi logla
#         vendor_name = product["id"].split("-")[0]
#         grouped_products.setdefault(vendor_name, []).append(product)

#     return {"data": grouped_products}






# @app.get("/proxy_image")
# async def proxy_image(url: str):

#     async with httpx.AsyncClient() as client:
#         response = await client.get(url)
#         if response.status_code == 200:
#             return StreamingResponse(
#                 response.aiter_bytes(),
#                 media_type=response.headers.get("content-type", "application/octet-stream"),
#             )
#         return {"error": "Unable to fetch image"}

# async def fetch_and_save_initial_products():
#     vendors, product_ids = get_all_vendors_and_product_ids()

#     for product_id in product_ids:
#         for vendor_name in vendors:
#             try:
#                 vendor_data = await get_product_from_vendor(vendor_name, product_id)
#                 standardized_data = map_vendor_data_to_standard(vendor_data, field_mapping)

#                 # ID oluşturuluyor
#                 standardized_data["id"] = f"{vendor_name}-{product_id}"

#                 # Varsayılan 'photos' ekleniyor
#                 standardized_data.setdefault("photos", ["https://parsadi.com/wp-content/uploads/2022/12/Vendor-.jpg"])
#                 print(f"[DEBUG] Created ID in fetch_and_save_initial_products: {standardized_data['id']}")

#                 await async_save_product_to_db(standardized_data, vendor_name)
#             except Exception as e:
#                 print(f"Error fetching product {product_id} from {vendor_name}: {e}")




# async def fetch_product_data(product_id: str):

#     vendor_calls = [
#         get_product_from_vendor(vendor, product_id) for vendor in ["vendor1", "vendor2", "vendor3"]
#     ]
#     responses = await asyncio.gather(*vendor_calls, return_exceptions=True)
#     data = []
#     for res in responses:
#         if isinstance(res, Exception):
#             print(f"Error fetching data: {res}")
#         elif res:
#             data.append(res)
#     return unify_data(data) if data else None

# def unify_data(data: list):

#     unified = []
#     for vendor_data in data:
#         if vendor_data:

#             standardized_data = map_vendor_data_to_standard(vendor_data, field_mapping)

#             photos = standardized_data.get("photos", ["https://parsadi.com/wp-content/uploads/2022/12/Vendor-.jpg"])
#             unified.append({
#                 "id": standardized_data.get("id"),
#                 "name": standardized_data.get("name"),
#                 "description": standardized_data.get("description", ""),
#                 "price": standardized_data.get("price", round(random.uniform(10, 100), 2)),
#                 "photos": photos,
#             })
#     return unified


from fastapi import FastAPI
from threading import Thread
from app.presentation.api.products import router as product_router
from app.presentation.api.health import router as health_router
from app.infrastructure.database.base import engine, Base
from app.infrastructure.kafka.consumer import kafka_consumer_thread
from app.config.settings import settings

app = FastAPI()

# API route'larını ekle
app.include_router(product_router, tags=["Products"])
app.include_router(health_router, tags=["Health"])

# Uygulama başlatıldığında çalışacak işlemler
@app.on_event("startup")
async def startup_event():
    """
    Uygulama başlatıldığında yapılacak işler:
    1. Veritabanı tablolarını oluştur.
    2. Kafka consumer'ı başlat.
    """
    # Veritabanı tablolarını oluştur
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Veritabanı tabloları başarıyla oluşturuldu!")

    # Kafka consumer thread'i başlat
    consumer_thread = Thread(target=kafka_consumer_thread, daemon=True)
    consumer_thread.start()
    print("Kafka consumer thread'i başlatıldı.")

# Uygulama kapandığında çalışacak işlemler
@app.on_event("shutdown")
async def shutdown_event():
    """
    Uygulama kapanırken yapılacak işler.
    """
    print("Uygulama kapanıyor...")

# Sağlık kontrolü endpoint'i
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Sağlık kontrolü endpoint'i.
    """
    return {"status": "ok", "environment": settings.ENVIRONMENT}
