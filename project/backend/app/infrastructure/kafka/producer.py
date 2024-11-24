from kafka import KafkaProducer
import json

KAFKA_TOPIC = "product_updates"
KAFKA_BROKER_URL = "kafka:9092"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER_URL],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def send_to_kafka(data: dict):
   
    try:
        producer.send(KAFKA_TOPIC, value=data)
        print(f"Data sent to Kafka topic '{KAFKA_TOPIC}': {data}")
    except Exception as e:
        print(f"Error sending data to Kafka: {e}")
        raise
