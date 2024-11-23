from kafka import KafkaConsumer
import json
import asyncio
from app.infrastructure.database.repositories import SQLAlchemyProductRepository
from app.infrastructure.database.base import get_db
from app.domain.models import Product
from app.domain.services import ProductService

KAFKA_TOPIC = "product_updates"
KAFKA_BROKER_URL = "kafka:9092"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="product_group",
    auto_offset_reset="earliest",
)


async def save_to_database(product_data: dict):
    """
    Kafka'dan alınan mesajları veritabanına kaydeder.
    """
    async for db_session in get_db():
        repository = SQLAlchemyProductRepository(db_session)
        service = ProductService(repository)

 
        product = Product(
            id=product_data["id"],
            name=product_data["name"],
            description=product_data.get("description", ""),
            price=product_data["price"],
            photos=product_data.get("photos", []),
        )
        await service.save_product(product)
        print(f"[DEBUG] Saved product to database: {product}")


def kafka_consumer_thread():
    """
    Kafka mesajlarını dinler ve işleme alır.
    """
    for message in consumer:
        product_data = message.value
        print(f"[DEBUG] Consumed from Kafka: {product_data}")
        asyncio.run(save_to_database(product_data))
