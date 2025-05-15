import random
import json

device_types = [
    "Infusion Pump", "ECG Monitor", "Ventilator",
    "Heart Rate Sensor", "Blood Pressure Monitor",
    "Oxygen Monitor", "Temperature Sensor"
]


def generate_hospital_rooms():
    hospital = {}
    ip_counter = 10  # starting IP suffix

    for room_num in range(1, 11):  # 10 rooms
        devices = []

        for i in range(7):  # 7 devices per room
            device_type = device_types[i % len(device_types)]

            # Randomly assign monitoring type for demo (50% SNMP, 50% CLI)
            monitor_type = random.choice(["snmp", "cli"])

            device = {
                "name": f"Room {room_num} - {device_type} {chr(65 + i)}",
                "ip": f"192.168.1.{ip_counter}",
                "device_type": device_type,
                "type": monitor_type,
                "thresholds": {
                    "cpu": random.randint(70, 90),
                    "ram": random.randint(70, 90),
                    "disk_usage": random.randint(70, 90),
                    "temperature": random.randint(70, 90),
                    "network_errors": random.randint(5, 15)
                },
                "metrics": {
                    "cpu": 0,
                    "ram": 0,
                    "disk_usage": 0,
                    "temperature": 0,
                    "uptime": 0,
                    "network_errors": 0
                }
            }

            # Add CLI auth info if CLI type
            if monitor_type == "cli":
                device["username"] = "admin"
                device["password"] = "password123"
            else:
                device["community"] = "public"  # SNMP community string

            devices.append(device)
            ip_counter += 1

        hospital[f"Room {room_num}"] = devices

    # Save to config file
    with open("config/hospital_devices.json", "w") as f:
        json.dump(hospital, f, indent=4)

    return hospital


if __name__ == "__main__":
    generate_hospital_rooms()
