import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque
import threading
import queue
import time

# Constants
MAX_DATA_POINTS = 20  # Number of points to show in graph window

class DeviceGraph:
    def __init__(self, parent, device_name):
        self.device_name = device_name
        self.frame = ttk.LabelFrame(parent, text=device_name)
        self.frame.pack(fill='x', padx=5, pady=5)

        self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 5))
        self.fig.tight_layout(pad=3.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack()

        # Data buffers
        self.cpu_data = deque(maxlen=MAX_DATA_POINTS)
        self.ram_data = deque(maxlen=MAX_DATA_POINTS)
        self.disk_data = deque(maxlen=MAX_DATA_POINTS)
        self.temp_data = deque(maxlen=MAX_DATA_POINTS)
        self.time_stamps = deque(maxlen=MAX_DATA_POINTS)

        # Init plots
        self.lines = {}
        self._init_plots()

    def _init_plots(self):
        metrics = ['CPU %', 'RAM %', 'Disk Usage %', 'Temperature °C']
        axs_flat = self.axs.flatten()
        for ax, metric in zip(axs_flat, metrics):
            ax.set_ylim(0, 110)
            ax.set_title(metric)
            ax.set_xlabel("Time")
            ax.set_ylabel(metric)
            line, = ax.plot([], [], 'b-')
            self.lines[metric] = line

    def update(self, metrics):
        # Add new data points
        now = time.strftime("%H:%M:%S")
        self.time_stamps.append(now)
        self.cpu_data.append(metrics.get('cpu', 0))
        self.ram_data.append(metrics.get('ram', 0))
        self.disk_data.append(metrics.get('disk_usage', 0))
        self.temp_data.append(metrics.get('temperature', 0))

        # Update line data
        self.lines['CPU %'].set_data(range(len(self.cpu_data)), self.cpu_data)
        self.lines['RAM %'].set_data(range(len(self.ram_data)), self.ram_data)
        self.lines['Disk Usage %'].set_data(range(len(self.disk_data)), self.disk_data)
        self.lines['Temperature °C'].set_data(range(len(self.temp_data)), self.temp_data)

        # Update axes limits and ticks
        for ax in self.axs.flatten():
            ax.set_xlim(0, MAX_DATA_POINTS)

        self.canvas.draw_idle()

class RoomTab:
    def __init__(self, notebook, room_name):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text=room_name)
        self.room_name = room_name
        self.device_graphs = {}

    def update_device(self, device_name, metrics):
        if device_name not in self.device_graphs:
            self.device_graphs[device_name] = DeviceGraph(self.frame, device_name)
        self.device_graphs[device_name].update(metrics)

class EyesMonGUI:
    def __init__(self, root, data_queue):
        self.root = root
        self.root.title("EyesMon Hospital Device Monitor")

        self.data_queue = data_queue

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill='both')

        self.rooms = {}  # room_name -> RoomTab

        # Start periodic GUI update
        self.root.after(1000, self.process_data_queue)

    def process_data_queue(self):
        while not self.data_queue.empty():
            data = self.data_queue.get()
            room = data['room']
            device = data['device_name']
            metrics = data['metrics']

            if room not in self.rooms:
                self.rooms[room] = RoomTab(self.notebook, room)

            self.rooms[room].update_device(device, metrics)

        self.root.after(1000, self.process_data_queue)  # schedule next check

def start_gui(data_queue):
    root = tk.Tk()
    gui = EyesMonGUI(root, data_queue)
    root.mainloop()

# For testing standalone
if __name__ == "__main__":
    import random

    q = queue.Queue()

    def fake_data_producer():
        rooms = ['Room 1', 'Room 2']
        devices = ['Infusion Pump A', 'Ventilator B']
        while True:
            for room in rooms:
                for device in devices:
                    metrics = {
                        "cpu": random.randint(10, 90),
                        "ram": random.randint(10, 90),
                        "disk_usage": random.randint(10, 90),
                        "temperature": random.randint(30, 80),
                        "uptime": random.randint(100, 5000),
                        "network_errors": random.randint(0, 5),
                    }
                    q.put({"room": room, "device_name": device, "metrics": metrics})
            time.sleep(5)

    threading.Thread(target=fake_data_producer, daemon=True).start()
    start_gui(q)
