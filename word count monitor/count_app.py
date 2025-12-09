import json
import os
from datetime import date
from threading import Thread
import time

from pynput import keyboard
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# --- Config ---
DATA_FILE = "word_count.json"

# --- Load or initialize data ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {}

today_str = str(date.today())
if today_str not in data:
    data[today_str] = 0

# --- Functions ---
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_icon_image(count):
    # Small square icon with the count
    img = Image.new("RGB", (64, 64), color="white")
    d = ImageDraw.Draw(img)
    text = str(count)
    d.text((10, 20), text, fill="black")
    return img

def update_icon(icon):
    icon.icon = create_icon_image(data[today_str])
    icon.title = f"Words today: {data[today_str]}"

def on_press(key):
    global data
    try:
        if key == keyboard.Key.space or key == keyboard.Key.enter:
            data[today_str] += 1
            save_data()
            update_icon(icon_instance)
    except Exception as e:
        print(f"Error: {e}")

def quit_app(icon, item):
    icon.stop()

# --- Midnight reset thread ---
def midnight_check():
    global today_str
    while True:
        time.sleep(10)  # check every 10 seconds
        current_day = str(date.today())
        if current_day != today_str:
            today_str = current_day
            if today_str not in data:
                data[today_str] = 0
            save_data()
            update_icon(icon_instance)

# --- Keyboard listener ---
listener = keyboard.Listener(on_press=on_press)
listener.start()

# --- System tray icon ---
menu = Menu(MenuItem("Quit", quit_app))
icon_instance = Icon("WordCount", create_icon_image(data[today_str]), "Word Count", menu)

# Start the midnight reset thread
Thread(target=midnight_check, daemon=True).start()

# --- Run icon ---
icon_instance.run()
