from fastapi import FastAPI, HTTPException, Query
import asyncio
import json
import httpx
import random
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.db import async_get_product_from_db, async_get_all_products, create_products_table, async_save_product_to_db
from app.kafka import send_to_kafka
from app.vendor_apis import get_product_from_vendor, get_all_vendors_and_product_ids


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await create_products_table()
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

    normalized_products = []
    for product in products:
        if "-" not in product["id"]:
            product["id"] = f"vendor4-{product['id']}"  
        normalized_products.append(product)

    grouped_products = {}
    for product in normalized_products:
        vendor_name = product["id"].split("-")[0]
        grouped_products.setdefault(vendor_name, []).append(product)
    
    return {"data": grouped_products}


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


@app.get("/proxy_image")
async def proxy_image(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return StreamingResponse(
                response.aiter_bytes(),
                media_type=response.headers.get("content-type", "application/octet-stream"),
            )
        return {"error": "Unable to fetch image"}


async def fetch_and_save_initial_products():
    """
    Tüm vendor ve ürün ID'lerini dinamik olarak işle ve verileri kaydet.
    """

    vendors, product_ids = get_all_vendors_and_product_ids()

    for product_id in product_ids:
        for vendor_name in vendors:
            try:
                vendor_data = await get_product_from_vendor(vendor_name, product_id)
                vendor_data.setdefault("photos", ["https://parsadi.com/wp-content/uploads/2022/12/Vendor-.jpg"])  
                vendor_data["price"] = round(random.uniform(10, 100), 2)  # Rastgele fiyat
                print(f"{vendor_name} response for product {product_id}: {vendor_data}")
                await async_save_product_to_db(vendor_data, vendor_name)
            except Exception as e:
                print(f"Error fetching product {product_id} from {vendor_name}: {e}")


async def fetch_product_data(product_id: str):
    vendor_calls = [
        get_product_from_vendor(vendor, product_id) for vendor in ["vendor1", "vendor2", "vendor3"]
    ]
    responses = await asyncio.gather(*vendor_calls, return_exceptions=True)
    data = []
    for res in responses:
        if isinstance(res, Exception):
            print(f"Error fetching data: {res}")
        elif res:
            data.append(res)
    return unify_data(data) if data else None


def unify_data(data: list):
    unified = []
    for vendor_data in data:
        if vendor_data:
            photos = vendor_data.get("photos", ["https://parsadi.com/wp-content/uploads/2022/12/Vendor-.jpg"])  # Varsayılan fotoğraf
            unified.append({
                "id": vendor_data.get("id"),
                "name": vendor_data.get("name"),
                "description": vendor_data.get("description", ""),
                "price": round(random.uniform(10, 100), 2),  # Rastgele fiyat
                "photos": photos,
            })
    return unified
