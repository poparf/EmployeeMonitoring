from pynput import mouse
import time
from threading import Thread


"""
We cannot store mouse events in a DB since they are too frequent.
So we will process them in real-time.

How to detect mouse jiggler ?
- if the movement pattern repeats
- ml anomaly detection
"""


def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0} at {1}'.format(
        'down' if dy < 0 else 'up',
        (x, y)))


mouseListener = mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll)
# You import the listener and start it in main
# listener.start()


# while(True):
#     time.sleep(1)