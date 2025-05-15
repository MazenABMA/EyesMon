import time
import os
import winsound
from monitor.simulator import simulate_device_polling

LOG_FILE = "logs/events.log"
os.makedirs("logs", exist_ok=True)


def log_alert(room, device, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [ALERT] {room} - {device} - {message}\n")


def play_alert_sound():
    # Beep sound for alerts
    winsound.Beep(1000, 500)  # 1000 Hz for 500 ms


def monitor_room(room_name, devices):
    cycle = 0
    while True:
        cycle += 1
        print(f"\nPolling devices... (Cycle {cycle})\n")

        for device in devices:
            device_id = device["name"]
            metrics = simulate_device_polling(device)

            cpu = metrics["cpu"]
            ram = metrics["ram"]
            cpu_threshold = device.get("cpu_threshold", 80)
            ram_threshold = device.get("ram_threshold", 80)

            alert_msgs = []
            alert_triggered = False

            if cpu >= cpu_threshold:
                msg = f"CPU is {cpu}%!"
                alert_msgs.append(msg)
                log_alert(room_name, device_id, msg)
                alert_triggered = True
            if ram >= ram_threshold:
                msg = f"RAM is {ram}%!"
                alert_msgs.append(msg)
                log_alert(room_name, device_id, msg)
                alert_triggered = True

            if alert_msgs:
                for msg in alert_msgs:
                    print(f"[ALERT] {room_name} - {device_id} - {msg}")
                play_alert_sound()  # 🔊 Alert sound
            elif cycle % 5 == 0:
                print(f"[OK] {room_name} - {device_id} - CPU: {cpu}%, RAM: {ram}%")

        print("-" * 50)
        time.sleep(2)
