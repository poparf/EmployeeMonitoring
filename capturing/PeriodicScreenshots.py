import io

import pyautogui
import time
from threading import Thread
from db.repository.PeriodScreenshotsRepository import PeriodicScreenshotsRepository

class PeriodicScreenshots(Thread):
    def __init__(self):
        super().__init__()
        self.interval = 10
        self.takeScreenshots = True

    def run(self):
        periodic_screenshots_repository = PeriodicScreenshotsRepository()
        while self.takeScreenshots:
            try:
                blob_data = io.BytesIO()
                screenshot = pyautogui.screenshot()
                screenshot.save(blob_data, format='PNG')
                blob_data = blob_data.getvalue()
                periodic_screenshots_repository = PeriodicScreenshotsRepository()
                periodic_screenshots_repository.insert_screenshot(blob_data, time.time())
                print("Inserted a screenshot!")
                time.sleep(self.interval * 60)
            except Exception as e:
                print(f"Screenshot error: {e}")
        
    def stop(self):
        self.takeScreenshots = False
