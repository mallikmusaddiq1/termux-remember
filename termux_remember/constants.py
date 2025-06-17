# termux_remember/constants.py
import os

BASE_DIR = os.path.expanduser("~/.termux_remember")
USER_FILE = os.path.join(BASE_DIR, "user.json")
MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")

version = "1.1.0"
author = "Mallik Mohammad Musaddiq"
email = "mallikmusaddiq1@gmail.com"
github = "https://github.com/mallikmusaddiq1/termux-remember"

# 📁 Ensure base directory and empty JSON files exist
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

for path in [USER_FILE, MEMORY_FILE]:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("{}")