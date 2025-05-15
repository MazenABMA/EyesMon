import time
import random
from alert.alert_manager import log_alert, play_alert_sound

def simulate_cli_polling(device):
    base = random.randint(30, 60)
    return {
        "cpu": base + random.randint(-3, 6),
        "ram": base + random.randint(-2, 5)
    }

def monitor_room(room_name, devices):
    cycle = 0
    while True:
        cycle += 1
        print(f"\n[CLI] Polling devices... (Cycle {cycle})\n")
        for device in devices:
            device_id = device["name"]
            metrics = simulate_cli_polling(device)

            cpu = metrics["cpu"]
            ram = metrics["ram"]
            cpu_threshold = device.get("cpu_threshold", 80)
            ram_threshold = device.get("ram_threshold", 80)

            if cpu >= cpu_threshold:
                msg = f"CPU is {cpu}%!"
                print(f"[ALERT][CLI] {room_name} - {device_id} - {msg}")
                log_alert(room_name, device_id, msg)
                play_alert_sound()

            if ram >= ram_threshold:
                msg = f"RAM is {ram}%!"
                print(f"[ALERT][CLI] {room_name} - {device_id} - {msg}")
                log_alert(room_name, device_id, msg)
                play_alert_sound()

            if cycle % 5 == 0:
                print(f"[OK][CLI] {room_name} - {device_id} - CPU: {cpu}%, RAM: {ram}%")
        print("-" * 50)
        time.sleep(2)
