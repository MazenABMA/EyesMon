# import time
# import random
# from alert.alert_manager import log_alert, play_alert_sound, print_device_status
#
#
# def poll_device_snmp(device):
#     """
#     Simulates SNMP polling with enhanced error handling
#     - Simulates 20% random failures
#     - Detects CPU timeout conditions (<90% threshold)
#     - Returns all zeros for error states
#     """
#     try:
#         # Simulate normal operation
#         cpu_value = random.randint(10, 76)
#
#         # Simulate timeout condition (CPU < 90% treated as failure)
#         if cpu_value < 80 and random.random() < 0.1:  # 10% chance of timeout
#             raise Exception(f"CPU timeout detected ({cpu_value}% < 90%)")
#
#         # Simulate random SNMP failure (20% chance)
#         if random.random() < 0.2:
#             raise Exception("SNMP protocol failure (simulated)")
#
#         return {
#             "cpu": cpu_value,
#             "ram": random.randint(10, 77),
#             "disk_usage": random.randint(10, 30),
#             "temperature": random.randint(30, 70),
#             "uptime": 3600,
#             "network_errors": 0
#         }
#
#     except Exception as e:
#         # Log detailed error information
#         error_msg = f"[SNMP CRITICAL] {str(e)} - Device unresponsive"
#         log_alert(device.get("room", "Unknown Room"),
#                   device["name"],
#                   error_msg)
#
#         # Return all zeros for error state
#         return {
#             "cpu": 0,
#             "ram": 0,
#             "disk_usage": 0,
#             "temperature": 0,
#             "uptime": 0,
#             "network_errors": 5  # High error count for failure state
#         }
#
#
# def monitor_room_snmp(room_name, devices, data_queue):
#     """
#     Continuous SNMP monitoring with enhanced error handling
#     - Processes devices in parallel
#     - Handles timeout conditions
#     - Maintains error state until recovery
#     """
#     cycle = 1
#     error_states = {}  # Track devices in error state
#
#     while True:
#         print(f"\n[SNMP] Polling cycle {cycle} for {room_name}\n")
#
#         for device in devices:
#             device_id = device["name"]
#
#             # Skip if in cooldown after error
#             if error_states.get(device_id, 0) > time.time():
#                 continue
#
#             metrics = poll_device_snmp(device)
#
#             # Check for error state (all zeros)
#             if all(v == 0 for v in metrics.values()):
#                 error_states[device_id] = time.time() + 30  # 30s cooldown
#                 print(f"[ERROR] {device_id} in error state - skipping checks")
#                 continue
#
#             print_device_status(room_name, device, metrics)
#
#             # GUI data pipeline
#             data_queue.put({
#                 "room": room_name,
#                 "device_name": device["name"],
#                 "metrics": metrics,
#                 "status": "error" if metrics["cpu"] == 0 else "normal"
#             })
#
#             # Threshold checks
#             alerts = []
#             if metrics["cpu"] >= device["thresholds"].get("cpu", 90):
#                 alerts.append(f"[SNMP ALERT] {device_id} - CPU overload ({metrics['cpu']}%)")
#             if metrics["ram"] >= device["thresholds"].get("ram", 90):
#                 alerts.append(f"[SNMP ALERT] {device_id} - RAM overload ({metrics['ram']}%)")
#
#             # Process alerts
#             for alert in alerts:
#                 print(alert)
#                 log_alert(room_name, device_id, alert)
#                 play_alert_sound()
#
#         print("=" * 50)
#         cycle += 1
#         time.sleep(10)  # Polling interval
import time
import random
import threading
import os
from queue import Queue
from alert.alert_manager import log_alert, play_alert_sound, print_device_status

# Global timeout tracking
device_timeout_states = {}
command_queue = Queue()


def reset_all_timeouts():
    """Reset all devices in timeout state"""
    count = sum(1 for state in device_timeout_states.values() if state)
    device_timeout_states.clear()
    return f"Reset {count} device(s) in timeout state"

# Update the command_listener function
def command_listener():
    """Runs in separate thread to handle commands"""
    while True:
        cmd = input("\nMonitorCMD> ").strip()
        if cmd.lower() == "list":
            print("Timed-out devices:", [d for d, s in device_timeout_states.items() if s])
        elif cmd == "reset all":  # New command
            print(reset_all_timeouts())
        elif cmd.startswith("reset "):
            print(reset_device_timeout(cmd[6:].strip()))
        elif cmd == "help":
            print("Available commands: reset [DEVICE], reset all, list, help, exit")
        elif cmd == "exit":
            os._exit(0)
def poll_device_snmp(device):
    """
    Persistent timeout version
    - Once CPU >80%, device stays in timeout state until manually reset
    """
    device_id = device["name"]

    try:
        # Check if device is in forced timeout state
        if device_timeout_states.get(device_id, False):
            raise Exception("Persistent timeout state (CPU previously >80%)")

        cpu_value = random.randint(10, 100)  # Full range up to 100%

        # Immediate timeout if CPU >80%
        if cpu_value > 80:
            device_timeout_states[device_id] = True  # Set persistent flag
            raise Exception(f"PERSISTENT TIMEOUT: CPU at {cpu_value}% > 80% threshold")

        return {
            "cpu": cpu_value,
            "ram": random.randint(10, 77),
            "disk_usage": random.randint(10, 30),
            "temperature": random.randint(30, 70),
            "uptime": 3600,
            "network_errors": 0
        }

    except Exception as e:
        error_msg = f"[HARD TIMEOUT] {str(e)}"
        log_alert(device.get("room", "Unknown Room"),
                  device["name"],
                  error_msg)

        return {
            "cpu": -1,  # Special error code
            "ram": -1,
            "disk_usage": -1,
            "temperature": -1,
            "uptime": 0,
            "network_errors": 10
        }


def monitor_room_snmp(room_name, devices, data_queue):
    # Start command listener thread
    threading.Thread(target=command_listener, daemon=True).start()

    cycle = 1
    while True:
        # Check for commands
        if not command_queue.empty():
            cmd = command_queue.get()
            if cmd.startswith("reset "):
                print(reset_device_timeout(cmd[6:].strip()))

        print(f"\n[SNMP] Polling Cycle {cycle}")
        for device in devices:
            metrics = poll_device_snmp(device)
            device_id = device["name"]

            if -1 in metrics.values():
                print(f"[HARD LOCK] {device_id}")
            else:
                print_device_status(room_name, device, metrics)

            data_queue.put({
                "room": room_name,
                "device_name": device_id,
                "metrics": metrics,
                "status": "timeout" if -1 in metrics.values() else "normal"
            })

        print("=" * 50)
        cycle += 1
        time.sleep(10)