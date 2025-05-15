import time
from monitor.simulator import simulate_device_polling

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
            if cpu >= cpu_threshold:
                alert_msgs.append(f"CPU is {cpu}%!")
            if ram >= ram_threshold:
                alert_msgs.append(f"RAM is {ram}%!")

            if alert_msgs:
                for msg in alert_msgs:
                    print(f"[ALERT] {room_name} - {device_id} - {msg}")
            elif cycle % 5 == 0:  # Print status every 5 cycles
                print(f"[OK] {room_name} - {device_id} - CPU: {cpu}%, RAM: {ram}%")

        print("-" * 50)
        time.sleep(2)