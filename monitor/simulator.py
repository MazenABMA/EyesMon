import random

def simulate_device_polling(device):
    device_type = device.get("type", "Generic")

    # Lower average usage depending on device type
    if device_type in ["Ventilator", "ECG Monitor", "Heart Rate Sensor"]:
        base_usage = random.randint(40, 65)
    else:
        base_usage = random.randint(30, 55)

    # Small fluctuation to simulate slight changes
    cpu_usage = base_usage + random.randint(-3, 4)
    ram_usage = base_usage + random.randint(-2, 4)

    # Occasionally spike one metric to simulate rare alert
    if random.random() < 0.05:  # 5% chance of spike
        if random.random() < 0.5:
            cpu_usage = random.randint(81, 95)
        else:
            ram_usage = random.randint(81, 95)

    # Clamp values
    cpu_usage = max(0, min(cpu_usage, 100))
    ram_usage = max(0, min(ram_usage, 100))

    return {
        "cpu": cpu_usage,
        "ram": ram_usage
    }