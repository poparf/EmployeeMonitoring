from kafkadir.KafkaProducerWrapper import KafkaProducerWrapper
import kafka.errors
import time
from threading import Thread, Lock

class KafkaConnectionChecker(Thread):
    no_brokers_available = False
    lock = Lock()
    
    def run(self):
        with KafkaConnectionChecker.lock:
            while(True):
                try:
                    kafka_producer = KafkaProducerWrapper(['localhost:9092'])
                    kafka_producer.close()
                    break
                except kafka.errors.NoBrokersAvailable:
                    print("No broker available.")
                    KafkaConnectionChecker.no_brokers_available = True
                    time.sleep(30)
    
    def __init__(self):
        super().__init__()
        