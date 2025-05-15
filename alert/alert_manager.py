import time
import os
import platform

LOG_PATH = "logs/events.log"

def ensure_log_path():
    log_dir = os.path.dirname(LOG_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def print_device_status(room, device, metrics):
    print(f"[OK] {room} - {device['name']} - CPU: {metrics.get('cpu', 'N/A')}%, "
          f"RAM: {metrics.get('ram', 'N/A')}%, Disk: {metrics.get('disk_usage', 'N/A')}%, "
          f"Temp: {metrics.get('temperature', 'N/A')}°C, Uptime: {metrics.get('uptime', 'N/A')}s, "
          f"Net Errors: {metrics.get('network_errors', 'N/A')}")

def check_alerts(device_name, metrics, thresholds):
    alerts = []

    if metrics.get("cpu", 0) > thresholds.get("cpu", 90):
        alerts.append(f"[ALERT] {device_name} - CPU usage high at {metrics['cpu']}%!")
    if metrics.get("ram", 0) > thresholds.get("ram", 90):
        alerts.append(f"[ALERT] {device_name} - RAM usage high at {metrics['ram']}%!")
    if metrics.get("disk_usage", 0) > thresholds.get("disk_usage", 90):
        alerts.append(f"[ALERT] {device_name} - Disk usage high at {metrics['disk_usage']}%!")
    if metrics.get("temperature", 0) > thresholds.get("temperature", 75):
        alerts.append(f"[ALERT] {device_name} - Temperature high at {metrics['temperature']}°C!")
    # Add more alert checks as needed

    return alerts

def log_alert(room, device_name, message):
    ensure_log_path()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"{timestamp} - ALERT - {room} - {device_name} - {message}\n"
    with open(LOG_PATH, "a") as f:
        f.write(log_msg)

def play_alert_sound():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 500)
    else:
        print('\a')