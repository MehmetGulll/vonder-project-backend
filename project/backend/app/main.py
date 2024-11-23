from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from threading import Thread
import httpx
from app.presentation.api.products import router as product_router
from app.presentation.api.health import router as health_router
from app.infrastructure.database.base import engine, Base
from app.infrastructure.kafka.consumer import kafka_consumer_thread
from app.config.settings import settings

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# API routers
app.include_router(product_router, tags=["Products"])
app.include_router(health_router, tags=["Health"])

@app.on_event("startup")
async def startup_event():
    """
    Uygulama başlatıldığında yapılacak işler:
    1. Veritabanı tablolarını oluştur.
    2. Kafka consumer'ı başlat.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Veritabanı tabloları başarıyla oluşturuldu!")

    consumer_thread = Thread(target=kafka_consumer_thread, daemon=True)
    consumer_thread.start()
    print("Kafka consumer thread'i başlatıldı.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Uygulama kapanırken yapılacak işler.
    """
    print("Uygulama kapanıyor...")


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Sağlık kontrolü endpoint'i.
    """
    return {"status": "ok", "environment": settings.ENVIRONMENT}


@app.get("/proxy_image")
async def proxy_image(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            print(f"Proxy response headers: {response.headers}")
            print(f"Proxy response content: {response.content[:100]}")  
            if "image" in response.headers.get("content-type", ""):
                return StreamingResponse(
                    response.aiter_bytes(),
                    media_type=response.headers["content-type"],
                )
            return {"error": "Invalid content type"}
        except Exception as e:
            print(f"Proxy error: {e}")
            return {"error": "Unable to fetch image"}
