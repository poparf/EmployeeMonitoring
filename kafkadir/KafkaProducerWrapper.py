from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import time

class KafkaProducerWrapper:
    """
    bootstrap_servers: list of kafka brokers
    example: [localhost:9092]
    """
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            # Ce se trimite va fi trimis in format json
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=3 # Se incearca trimiterea mesajului de 3 ori
        )
        
    def send_message(self, topic, data):
        try:
            future = self.producer.send(topic, data)
            self.producer.flush()
            return future.get()
        except KafkaError as e:
            # TODO:Logging error
            print(f"Kafka error: {e}")
            return None
        
    def close(self):
        self.producer.close()