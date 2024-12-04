import pyautogui
import time
from threading import Thread

class PeriodicScreenshots(Thread):
    def __init__(self):
        super().__init__()
        self.interval = 10 # minutes
        self.takeScreenshots = True
        
    def run(self):
        while self.takeScreenshots:
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save(f"screenshot_{int(time.time())}.png")
                time.sleep(self.interval)
            except Exception as e:
                print(f"Screenshot error: {e}")
        
    def stop(self):
        self.takeScreenshots = False

if __name__ == '__main__':
    screenshot_thread = PeriodicScreenshots()
    screenshot_thread.start()
    time.sleep(30)
    screenshot_thread.stop()    
    