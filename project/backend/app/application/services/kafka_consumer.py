from app.infrastructure.kafka.consumer import kafka_consumer_thread


def start_kafka_consumer() -> None:
    """
    Kafka consumer thread'i başlatır.

    Bu işlev, Kafka'daki "product_updates" konusundaki mesajları okumak ve işlemek için
    bir thread başlatır. Tüketici bağlantı problemleri oluştuğunda hata çıktısı verir.
    """
    try:
        print("Starting Kafka consumer thread...")
        kafka_consumer_thread()
    except Exception as e:
        print(f"Error starting Kafka consumer thread: {e}")
