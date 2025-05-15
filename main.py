import json
import threading
from monitor.snmp_monitor import monitor_room_snmp
from monitor.cli_monitor import monitor_room_cli
import time

def load_devices():
    with open("config/hospital_devices.json") as f:
        hospital = json.load(f)
    return hospital

def start_monitoring():
    hospital = load_devices()
    rooms = list(hospital.keys())

    print("Available rooms:")
    for i, room in enumerate(rooms, 1):
        print(f"{i}. {room}")

    selected_input = input("Enter room numbers to monitor (comma separated), or 'all' to monitor all rooms: ").strip()

    if selected_input.lower() == "all":
        selected_rooms = rooms
    else:
        try:
            indices = [int(x.strip()) for x in selected_input.split(",")]
            selected_rooms = [rooms[i - 1] for i in indices if 0 < i <= len(rooms)]
        except Exception:
            print("Invalid input. Monitoring all rooms by default.")
            selected_rooms = rooms

    for room_name in selected_rooms:
        devices = hospital[room_name]
        snmp_devices = [d for d in devices if d["type"] == "snmp"]
        cli_devices = [d for d in devices if d["type"] == "cli"]

        if snmp_devices:
            threading.Thread(target=monitor_room_snmp, args=(room_name, snmp_devices), daemon=True).start()
        if cli_devices:
            threading.Thread(target=monitor_room_cli, args=(room_name, cli_devices), daemon=True).start()

    # Keep main thread alive so threads keep running
    while True:
        time.sleep(1)

if __name__ == "__main__":
    start_monitoring()