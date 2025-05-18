import time
from alert.alert_manager import log_alert, play_alert_sound

from alert.alert_manager import print_device_status
import random
from alert.alert_manager import log_alert

def poll_device_snmp(device):
    try:
        # Simulate SNMP failure 1 out of every 5 calls
        if random.random() < 0.2:
            raise Exception("Simulated SNMP failure")

        return {
            "cpu": random.randint(10, 95),
            "ram": random.randint(10, 95),
            "disk_usage": random.randint(10, 30),
            "temperature": random.randint(30, 70),
            "uptime": 3600,
            "network_errors": 0
        }

    except Exception as e:
        log_alert(device.get("room", "Unknown Room"), device["name"], f"[SNMP ERROR] {str(e)}")
        return {
            "cpu": 0,
            "ram": 0,
            "disk_usage": 0,
            "temperature": 0,
            "uptime": 0,
            "network_errors": 1
        }

import time

def monitor_room_snmp(room_name, devices, data_queue):
    cycle = 1
    while True:
        print(f"\n[SNMP] Polling devices... (Cycle {cycle})\n")
        for device in devices:
            metrics = poll_device_snmp(device)
            print_device_status(room_name, device, metrics)

            # Push data to GUI queue
            data_queue.put({
                "room": room_name,
                "device_name": device["name"],
                "metrics": metrics,
            })

            alerts = []
            if metrics["cpu"] > device["thresholds"].get("cpu", 100):
                alerts.append(f"[ALERT][SNMP] {room_name} - {device['name']} - CPU at {metrics['cpu']}%!")
            if metrics["ram"] > device["thresholds"].get("ram", 100):
                alerts.append(f"[ALERT][SNMP] {room_name} - {device['name']} - RAM at {metrics['ram']}%!")

            for alert in alerts:
                print(alert)
                log_alert(room_name, device['name'], alert)
                play_alert_sound()

        print("=" * 50)
        cycle += 1
        time.sleep(10)