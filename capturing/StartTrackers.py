from capturing.KeyboardTracker import keyboardListener
#from capturing.MouseTracker import mouseListener
from capturing.SystemTracker import SystemTracker
from capturing.WindowTracker import WindowTracker
from capturing.PeriodicScreenshots import PeriodicScreenshots

systemTracker = SystemTracker()
windowTracker = WindowTracker()
periodicScreenshots = PeriodicScreenshots()

def start_system_tracker():
    systemTracker.start()
    systemTracker.join()

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