from fastapi import FastAPI, HTTPException, Query
import asyncio
from app.db import async_get_product_from_db, async_get_all_products, create_products_table, async_save_product_to_db
from app.vendor_apis import vendor1, vendor2, vendor3
from app.kafka import send_to_kafka

app = FastAPI()

vendor_apis = [vendor1, vendor2, vendor3]


@app.on_event("startup")
async def startup_event():
    # Veritabanı bağlantısını kontrol et ve tabloyu oluştur
    await create_products_table()

    # Tedarikçi API'lerinden ürünleri çek ve veritabanına ekle
    await fetch_and_save_initial_products()





@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/products")
async def get_all_products(
    limit: int = Query(10, description="Number of products to return"),
    offset: int = Query(0, description="Number of products to skip")
):
    products = await async_get_all_products(limit, offset)
    if not products:
        return {"message": "No products found"}
    return products


@app.get("/product/{product_id}")
async def get_product(product_id: str):
    product = await async_get_product_from_db(product_id)
    if product:
        return product

    product_data = await fetch_product_data(product_id)
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await send_to_kafka(product_data)
    await async_save_product_to_db(product_data)
    return product_data


async def fetch_and_save_initial_products():
    product_ids = ["1", "2", "3", "4", "5"]  # Örnek ürün ID'leri

    for product_id in product_ids:
        product_data = await fetch_product_data(product_id)
        if product_data:
            for product in product_data:  # Tedarikçiden birden fazla ürün dönebilir
                await async_save_product_to_db(product)


async def fetch_product_data(product_id: str):
    vendor_calls = [vendor.get_product(product_id) for vendor in vendor_apis]
    responses = await asyncio.gather(*vendor_calls, return_exceptions=True)
    
    data = []
    for res in responses:
        if isinstance(res, Exception):
            print(f"Error fetching data from vendor: {res}")
        elif res:
            data.append(res)
    
    if not data:
        return None
    
    return unify_data(data)


def unify_data(data: list):
    unified = []
    for vendor_data in data:
        if vendor_data:
            unified.append({
                "id": vendor_data.get("id"),
                "name": vendor_data.get("name"),
                "description": vendor_data.get("description", ""),
                "price": vendor_data.get("price"),
                "photos": vendor_data.get("photos", []),
            })
    return unified
