from app.infrastructure.kafka.consumer import kafka_consumer_thread


def start_kafka_consumer() -> None:
    try:
        print("Starting Kafka consumer thread...")
        kafka_consumer_thread()
    except Exception as e:
        print(f"Error starting Kafka consumer thread: {e}")
