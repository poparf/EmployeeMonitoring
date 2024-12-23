import io

import pyautogui
import time
from threading import Thread
from db.repository.PeriodScreenshotsRepository import PeriodicScreenshotsRepository
from kafkadir.KafkaProducerWrapper import KafkaProducerWrapper
import base64

class PeriodicScreenshots(Thread):
    def __init__(self):
        super().__init__()
        self.interval = 10
        self.takeScreenshots = True
        self.periodic_screenshots_repository = PeriodicScreenshotsRepository()
        self.kafka_producer = KafkaProducerWrapper(['localhost:9092'])
        

    def run(self):
        periodic_screenshots_repository = PeriodicScreenshotsRepository()
        while self.takeScreenshots:
            try:
                blob_data = io.BytesIO()
                screenshot = pyautogui.screenshot()
                screenshot.save(blob_data, format='JPEG', quality=10)
                blob_data = blob_data.getvalue()
                payload = {
                    "screenshot": base64.b64encode(blob_data).decode('utf-8'),
                    "timestamp": time.time()
                }
                self.periodic_screenshots_repository.insert_screenshot(payload["screenshot"], payload["timestamp"])
                self.kafka_producer.send_message(KafkaProducerWrapper.SCREENSHOT_TOPIC, payload)
                print("Inserted a screenshot!")
                time.sleep(self.interval * 60)
            except Exception as e:
                print(f"Screenshot error: {e}")
        
    def stop(self):
        self.takeScreenshots = False
        self.kafka_producer.close()
