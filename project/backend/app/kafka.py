from kafka import KafkaProducer, KafkaConsumer
import json
from threading import Thread
import asyncio
from app.db import async_save_product_to_db  

KAFKA_TOPIC = "product_updates"
KAFKA_BROKER_URL = "kafka:9092"


producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="product_group",
    auto_offset_reset="earliest",
)


def kafka_consumer_thread():

    for message in consumer:
        product_data = message.value
        vendor_name = product_data.get("vendor", "unknown_vendor")
        asyncio.run(async_save_product_to_db(product_data, vendor_name))
        print(f"Saved product to database: {product_data}")


def send_to_kafka(data):

    producer.send(KAFKA_TOPIC, value=data)
