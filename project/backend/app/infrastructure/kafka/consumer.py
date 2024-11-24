from kafka import KafkaConsumer
import json
import asyncio
from app.infrastructure.database.database_adapter import async_save_product_to_db

KAFKA_TOPIC = "product_updates"
KAFKA_BROKER_URL = "kafka:9092"


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="product_group",
    auto_offset_reset="earliest",
)


async def process_kafka_message(message: dict):
    """
    Kafka'dan gelen mesajı işle ve veritabanına kaydet.
    """
    try:
        vendor_name = message.get("vendor", "unknown_vendor")
        await async_save_product_to_db(message, vendor_name)
        print(f"Saved product to database: {message}")
    except Exception as e:
        print(f"Error processing Kafka message: {e}")
        raise


def kafka_consumer_thread():
    """
    Kafka Consumer için bir thread başlat.
    """
    print("Starting Kafka Consumer...")
    for message in consumer:
        product_data = message.value
        asyncio.run(process_kafka_message(product_data))
