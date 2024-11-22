from fastapi import FastAPI, HTTPException, Query
import asyncio
import json
import httpx
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.vendor_apis.vendor1 import get_product as vendor1_get_product
from app.vendor_apis.vendor2 import get_product as vendor2_get_product
from app.vendor_apis.vendor3 import get_product as vendor3_get_product
from app.db import async_get_product_from_db, async_get_all_products, create_products_table, async_save_product_to_db
from app.kafka import send_to_kafka

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vendor_apis = [vendor1_get_product, vendor2_get_product, vendor3_get_product]

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
    grouped_products = {}
    for product in products:
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
    """Başlangıçta tüm vendor'lardan ürünleri çekip kaydeder."""
    product_ids = ["1", "2", "3", "4", "5"] 

    for product_id in product_ids:
        for index, vendor in enumerate(vendor_apis):
            try:
                vendor_name = f"Vendor{index + 1}"
                vendor_data = await vendor(product_id) 
                print(f"{vendor_name} response for product {product_id}: {vendor_data}") 
                await async_save_product_to_db(vendor_data, vendor_name)
            except Exception as e:
                print(f"Error fetching product {product_id} from vendor {index + 1}: {e}")


async def fetch_product_data(product_id: str):
    vendor_calls = [vendor(product_id) for vendor in vendor_apis]
    responses = await asyncio.gather(*vendor_calls, return_exceptions=True)
    
    data = []
    for index, res in enumerate(responses):
        if isinstance(res, Exception):
            print(f"Error fetching data from vendor {index + 1}: {res}")
        elif res:
            print(f"Vendor {index + 1} response for product {product_id}: {res}")
            data.append(res)
    
    if not data:
        return None
    
    return unify_data(data)


def unify_data(data: list):
    unified = []
    for vendor_data in data:
        if vendor_data:
            photos = vendor_data.get("photos", [])
      
            if isinstance(photos, str):
                try:
                    photos = json.loads(photos) 
                except json.JSONDecodeError:
                    photos = [] 

            unified.append({
                "id": vendor_data.get("id"),
                "name": vendor_data.get("name"),
                "description": vendor_data.get("description", ""),
                "price": vendor_data.get("price"),
                "photos": photos, 
            })
    return unified
