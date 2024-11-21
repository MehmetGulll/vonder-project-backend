from kafka import KafkaProducer, KafkaConsumer
import json

KAFKA_TOPIC = "product_updates"

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer = lambda v: json.dumps(v).encode("utf-8"),
)

def send_to_kafka(data):
    producer.send(KAFKA_TOPIC, value=data)