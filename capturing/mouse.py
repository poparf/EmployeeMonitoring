from pynput import mouse
import time

timer = 0

def on_move(x, y):
    global timer
    timer = 0

def on_click(x, y, button, pressed):
    global timer
    timer = 0

def on_scroll(x, y, dx, dy):
    global timer
    timer = 0
    
listener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
listener.start()

while(True):
    time.sleep(1)
    timer = timer + 1
    print(timer)
    
    if(timer == 30):
        print("30 seconds have passed")
        # do something
    
    if(timer == 60 * 5):
        print("5 minutes have passed.")
        # do something
    