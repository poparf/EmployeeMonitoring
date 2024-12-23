
from capturing.KeyboardTracker import keyboardListener
print("Imported keyboardtracker")
#from capturing.MouseTracker import mouseListener
from capturing.SystemTracker import SystemTracker
print("Started system tracker")
from capturing.WindowTracker import WindowTracker
print("Started capturing windows")
from capturing.PeriodicScreenshots import PeriodicScreenshots
print("Started periodic screenshots")

windowTracker = WindowTracker()
periodicScreenshots = PeriodicScreenshots()

def start_trackers():
    windowTracker.start()
    #mouseListener.start()
    keyboardListener.start()
    periodicScreenshots.start()

def stop_trackers():
    windowTracker.stop()
    #mouseListener.stop()
    keyboardListener.stop()
    periodicScreenshots.stop()