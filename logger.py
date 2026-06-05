import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/transfer.log"

def log_event(message):
    time_info = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{time_info}] {message}\n")