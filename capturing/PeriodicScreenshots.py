import io

import pyautogui
import time
from threading import Thread
from db.repository.PeriodScreenshotsRepository import PeriodicScreenshotsRepository

class PeriodicScreenshots(Thread):
    def __init__(self):
        super().__init__()
        self.interval = 10 # minutes
        self.takeScreenshots = True
        self.periodic_screenshots_repository = PeriodicScreenshotsRepository()

    def run(self):
        while self.takeScreenshots:
            try:
                blob_data = io.BytesIO()
                screenshot = pyautogui.screenshot()
                screenshot.save(blob_data, format='PNG')
                blob_data = blob_data.getvalue()
                self.periodic_screenshots_repository.insert_screenshot(blob_data, time.time())
                time.sleep(self.interval)
            except Exception as e:
                print(f"Screenshot error: {e}")
        
    def stop(self):
        self.takeScreenshots = False