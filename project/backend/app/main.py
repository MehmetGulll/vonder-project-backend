from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from app.infrastructure.database.tables import create_products_table
from app.application.use_cases.sync_products import fetch_and_save_initial_products
from app.application.services.kafka_consumer import start_kafka_consumer
from app.application.use_cases.get_all_products import get_all_products

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

    kafka_thread = Thread(target=start_kafka_consumer)
    kafka_thread.start()

    await fetch_and_save_initial_products()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/products")
async def products_endpoint(
    limit: int = Query(10, description="Kaç ürün döndürülecek"),
    offset: int = Query(0, description="Kaç ürün atlanacak")
):
    try:
        products = await get_all_products(limit, offset)
        return products
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

@app.get("/proxy_image")
async def proxy_image(url: str):
 
    try:
 
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        

        if response.status_code == 200:
            return StreamingResponse(
                response.aiter_bytes(),
                media_type=response.headers.get("content-type", "image/jpeg"),
            )
        else:
            return {"error": f"Failed to fetch image. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": f"An error occurred while fetching the image: {str(e)}"}