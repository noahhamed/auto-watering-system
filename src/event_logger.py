from datetime import datetime


LOG_FILE = "watering_events.log"


def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as file:
        file.write(f"{timestamp} - {message}\n")