import time
import random
from alert.alert_manager import log_alert, play_alert_sound
import paramiko  # for SSH if you want real CLI polling
from alert.alert_manager import print_device_status
import time
import random
from alert.alert_manager import log_alert, play_alert_sound, print_device_status

def poll_device_cli(device):
    # Simulate or implement SSH command polling here, return metrics dict
    base = random.randint(30, 75)
    cpu = base + random.randint(-3, 6)
    ram = base + random.randint(-2, 6)

    if random.random() < 0.025:
        if random.random() < 0.5:
            cpu = random.randint(81, 95)
        else:
            ram = random.randint(81, 95)

    return {
        "cpu": min(cpu, 100),
        "ram": min(ram, 100),
        "disk_usage": random.randint(10, 30),
        "temperature": random.randint(30, 85),
        "uptime": random.randint(1, 1000),
        "network_errors": random.randint(0, 5)
    }

def monitor_room_cli(room_name, devices, data_queue):
    cycle = 1
    while True:
        print(f"\n[CLI] Polling devices... (Cycle {cycle})\n")
        for device in devices:
            metrics = poll_device_cli(device)
            print_device_status(room_name, device, metrics)

            # Push data to GUI queue
            data_queue.put({
                "room": room_name,
                "device_name": device["name"],
                "metrics": metrics,
            })

            alerts = []
            if metrics["cpu"] > device["thresholds"].get("cpu", 100):
                alerts.append(f"[ALERT][CLI] {room_name} - {device['name']} - CPU at {metrics['cpu']}%!")
            if metrics["ram"] > device["thresholds"].get("ram", 100):
                alerts.append(f"[ALERT][CLI] {room_name} - {device['name']} - RAM at {metrics['ram']}%!")

            for alert in alerts:
                print(alert)
                log_alert(room_name, device['name'], alert)
                play_alert_sound()

        print("=" * 50)
        cycle += 1
        time.sleep(10)
