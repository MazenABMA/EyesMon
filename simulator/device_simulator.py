# simulator/device_simulator.py

import random
import json

device_types = ["Infusion Pump", "ECG Monitor", "Ventilator", "Heart Rate Sensor", "Blood Pressure Monitor"]

def generate_hospital_rooms():
    hospital = {}
    ip_counter = 10

    for room_num in range(1, 11):  # 10 rooms
        device_count = random.randint(1, 7)
        devices = []

        for i in range(device_count):
            device = {
                "name": f"Room {room_num} - {device_types[i % len(device_types)]} {chr(65+i)}",
                "ip": f"192.168.1.{ip_counter}",
                "type": device_types[i % len(device_types)],
                "thresholds": {
                    "cpu": random.randint(70, 90),
                    "ram": random.randint(70, 90)
                }
            }
            ip_counter += 1
            devices.append(device)

        hospital[f"Room {room_num}"] = devices

    # Save to config file
    with open("config/hospital_devices.json", "w") as f:
        json.dump(hospital, f, indent=4)

    return hospital