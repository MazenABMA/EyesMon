# import time
# import random
# from alert.alert_manager import log_event
#
# def simulate_metrics():
#     return {
#         "cpu": random.randint(30, 100),
#         "ram": random.randint(30, 100)
#     }
#
# def check_device_health(device):
#     metrics = simulate_metrics()
#     for metric in ['cpu', 'ram']:
#         value = metrics[metric]
#         if value >= 80:
#             print(f"[ALERT] {device['name']} - {metric.upper()} is {value}%!")
#             log_event(device, metric, value)
#         else:
#             print(f"[OK] {device['name']} - {metric.upper()} is {value}%")
#     print()
#
# def monitor_room(devices):
#     print("📡 Starting real-time monitoring... Press CTRL+C to stop.\n")
#     try:
#         while True:
#             print("\nPolling devices...\n")
#             for device in devices:
#                 check_device_health(device)
#             time.sleep(2)
#     except KeyboardInterrupt:
#         print("\n🛑 Monitoring stopped by user.")