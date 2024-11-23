from kafka import KafkaProducer
import json

KAFKA_TOPIC = "product_updates"
KAFKA_BROKER_URL = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def send_to_kafka(data: dict):
    """
    Kafka'ya mesaj gönderir.
    """
    producer.send(KAFKA_TOPIC, value=data)
    print(f"[DEBUG] Sent to Kafka: {data}")
