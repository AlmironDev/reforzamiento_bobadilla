import psutil
import time
from tabulate import tabulate
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    return cpu_percent

def get_memory_info():
    memory_info = psutil.virtual_memory()
    return memory_info

def get_disk_info():
    disk_usage = psutil.disk_usage('/')
    return disk_usage

def get_network_info():
    net_info = psutil.net_io_counters()
    return net_info

def get_process_info():
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
        processes.append(proc.info)
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:10]  # Mostrar los 10 procesos con mayor uso de CPU

def display_info():
    while True:
        clear_terminal()

        # Información de CPU
        cpu_info = get_cpu_info()
        print("CPU Usage per Core:")
        for i, percent in enumerate(cpu_info):
            print(f"Core {i}: {percent}%")

        # Información de Memoria
        memory_info = get_memory_info()
        print("\nMemory Usage:")
        print(f"Total: {memory_info.total / (1024 ** 3):.2f} GB")
        print(f"Used: {memory_info.used / (1024 ** 3):.2f} GB")
        print(f"Free: {memory_info.free / (1024 ** 3):.2f} GB")
        print(f"Percentage: {memory_info.percent}%")

        # Información de Disco
        disk_info = get_disk_info()
        print("\nDisk Usage:")
        print(f"Total: {disk_info.total / (1024 ** 3):.2f} GB")
        print(f"Used: {disk_info.used / (1024 ** 3):.2f} GB")
        print(f"Free: {disk_info.free / (1024 ** 3):.2f} GB")
        print(f"Percentage: {disk_info.percent}%")

        # Información de Red
        net_info = get_network_info()
        print("\nNetwork IO:")
        print(f"Bytes Sent: {net_info.bytes_sent / (1024 ** 2):.2f} MB")
        print(f"Bytes Received: {net_info.bytes_recv / (1024 ** 2):.2f} MB")

        # Información de Procesos
        process_info = get_process_info()
        print("\nTop 10 Processes by CPU Usage:")
        table = [[proc['pid'], proc['name'], proc['cpu_percent'], proc['memory_info'].rss / (1024 ** 2)] for proc in process_info]
        print(tabulate(table, headers=['PID', 'Name', 'CPU %', 'Memory (MB)']))

        time.sleep(2)  # Refrescar cada 2 segundos

if __name__ == "__main__":
    display_info()







