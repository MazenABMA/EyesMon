import json
from monitor.snmp_monitor import monitor_room  # Using SNMP monitor


def load_devices():
    with open("config/hospital_devices.json") as f:
        return json.load(f)


def choose_room(devices_data):
    print("🏥 Available Rooms in Hospital:\n")
    for room in devices_data.keys():
        print(f"  {room}")
    choice = input("\n🔍 Enter a room number to monitor (e.g., 1): ")
    room_key = f"Room {choice}"
    if room_key in devices_data:
        return room_key, devices_data[room_key]
    else:
        print("❌ Invalid room number.")
        exit(1)


if __name__ == "__main__":
    devices_data = load_devices()
    room_name, devices = choose_room(devices_data)
    print(f"\n📡 Monitoring devices in {room_name}...\n")
    monitor_room(room_name, devices)
