def print_device_status(room_name, device, metrics):
    print(f"[{room_name}] Device: {device['name']} ({device['ip']})")
    for metric, value in metrics.items():
        print(f"  {metric}: {value}")
    print("-" * 40)