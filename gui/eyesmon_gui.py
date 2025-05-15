import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque
import threading
import queue
import time
import random

MAX_DATA_POINTS = 20

class DeviceGraph:
    def __init__(self, parent, device_name):
        self.device_name = device_name
        self.frame = ttk.LabelFrame(parent, text=device_name)
        # Don't pack here; will be controlled externally

        self.fig, self.axs = plt.subplots(2, 2, figsize=(7, 5))
        self.fig.tight_layout(pad=3.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack()

        self.cpu_data = deque(maxlen=MAX_DATA_POINTS)
        self.ram_data = deque(maxlen=MAX_DATA_POINTS)
        self.disk_data = deque(maxlen=MAX_DATA_POINTS)
        self.temp_data = deque(maxlen=MAX_DATA_POINTS)
        self.counter = 0

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
            ax.grid(True)
            line, = ax.plot([], [], 'b-')
            self.lines[metric] = line

    def update(self, metrics):
        self.counter += 1
        self.cpu_data.append(metrics.get('cpu', 0))
        self.ram_data.append(metrics.get('ram', 0))
        self.disk_data.append(metrics.get('disk_usage', 0))
        self.temp_data.append(metrics.get('temperature', 0))

        start_x = max(0, self.counter - len(self.cpu_data) + 1)
        x_vals = list(range(start_x, start_x + len(self.cpu_data)))

        self.lines['CPU %'].set_data(x_vals, self.cpu_data)
        self.lines['RAM %'].set_data(x_vals, self.ram_data)
        self.lines['Disk Usage %'].set_data(x_vals, self.disk_data)
        self.lines['Temperature °C'].set_data(x_vals, self.temp_data)

        for ax in self.axs.flatten():
            ax.set_xlim(start_x, start_x + MAX_DATA_POINTS)

        self.canvas.draw_idle()

class RoomTab:
    def __init__(self, notebook, room_name):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text=room_name)
        self.room_name = room_name

        self.device_graphs = {}
        self.device_names = []
        self.current_index = 0

        # Navigation buttons frame
        nav_frame = ttk.Frame(self.frame)
        nav_frame.pack(side='top', fill='x')

        self.prev_button = ttk.Button(nav_frame, text="◀ Previous", command=self.show_prev_device)
        self.prev_button.pack(side='left')

        self.device_label = ttk.Label(nav_frame, text="No devices yet")
        self.device_label.pack(side='left', expand=True, padx=10)

        self.next_button = ttk.Button(nav_frame, text="Next ▶", command=self.show_next_device)
        self.next_button.pack(side='right')

        # Container for graph frames
        self.graph_container = ttk.Frame(self.frame)
        self.graph_container.pack(expand=True, fill='both')

    def update_device(self, device_name, metrics):
        if device_name not in self.device_graphs:
            graph = DeviceGraph(self.graph_container, device_name)
            self.device_graphs[device_name] = graph
            graph.frame.pack_forget()  # Hide initially
            self.device_names.append(device_name)

        self.device_graphs[device_name].update(metrics)

        # Show first device initially or current device if updated
        if len(self.device_names) == 1:
            self.current_index = 0
            self.show_device_by_index(self.current_index)
        elif device_name == self.device_names[self.current_index]:
            self.show_device_by_index(self.current_index)

    def show_device_by_index(self, index):
        # Hide all device graphs
        for graph in self.device_graphs.values():
            graph.frame.pack_forget()

        # Show selected device graph
        current_device = self.device_names[index]
        self.device_graphs[current_device].frame.pack(expand=True, fill='both')
        self.device_label.config(text=f"Device: {current_device}")

        # Button state
        self.prev_button.config(state='normal' if index > 0 else 'disabled')
        self.next_button.config(state='normal' if index < len(self.device_names) - 1 else 'disabled')

    def show_prev_device(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_device_by_index(self.current_index)

    def show_next_device(self):
        if self.current_index < len(self.device_names) - 1:
            self.current_index += 1
            self.show_device_by_index(self.current_index)

class EyesMonGUI:
    def __init__(self, root, data_queue):
        self.root = root
        self.root.title("EyesMon Hospital Device Monitor")

        self.data_queue = data_queue

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=1, fill='both')

        self.rooms = {}

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

        self.root.after(1000, self.process_data_queue)

def start_gui(data_queue):
    root = tk.Tk()
    gui = EyesMonGUI(root, data_queue)
    root.mainloop()

if __name__ == "__main__":
    q = queue.Queue()

    def fake_data_producer():
        rooms = ['Room 1', 'Room 2']
        devices = ['Infusion Pump A', 'Ventilator B', 'ECG Monitor C']
        while True:
            for room in rooms:
                for device in devices:
                    metrics = {
                        "cpu": random.randint(10, 90),
                        "ram": random.randint(10, 90),
                        "disk_usage": random.randint(10, 90),
                        "temperature": random.randint(30, 80),
                    }
                    q.put({"room": room, "device_name": device, "metrics": metrics})
            time.sleep(5)

    threading.Thread(target=fake_data_producer, daemon=True).start()
    start_gui(q)
