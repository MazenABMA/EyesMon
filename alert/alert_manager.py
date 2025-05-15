import os
from datetime import datetime

LOG_PATH = "logs/events.log"

def check_alerts(device, metrics):
    for key in ['cpu', 'ram']:
        if metrics[key] >= device["thresholds"][key] or metrics[key] >= 80:
            log_event(device, key, metrics[key])
            print(f"[ALERT] {device['name']} - {key.upper()} is {metrics[key]}%!")
        else:
            print(f"[OK] {device['name']} - {key.upper()} is {metrics[key]}%")

def log_event(device, metric, value):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"{timestamp} - ALERT - {device['name']} - {metric.upper()} usage is {value}%\n")

