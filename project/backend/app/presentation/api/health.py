from fastapi import APIRouter, Depends
from app.infrastructure.database.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from kafka import KafkaProducer

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Sağlık kontrolü endpoint'i.
    """
    # Veritabanı kontrolü
    try:
        await db.execute("SELECT 1")  # Basit bir sorgu
    except Exception as e:
        return {"status": "error", "database": str(e)}

    # Kafka kontrolü
    try:
        producer = KafkaProducer(bootstrap_servers=["kafka:9092"])
        producer.close()  # Sadece bağlantıyı test ediyoruz
    except Exception as e:
        return {"status": "error", "kafka": str(e)}

    return {"status": "ok", "database": "connected", "kafka": "connected"}
