import docker
from datetime import datetime, timezone

def format_uptime(start_time):
    """Formato el tiempo desde que el contenedor ha estado en ejecución."""
    now = datetime.now(timezone.utc)
    uptime = now - start_time
    seconds = int(uptime.total_seconds())

    if seconds < 60:
        return f"{seconds} secs"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} mins"
    elif seconds < 86400:
        hours, remainder = divmod(seconds, 3600)
        minutes = remainder // 60
        return f"{hours} hrs {minutes} mins"
    else:
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes = remainder // 60
        return f"{days} days {hours} hrs {minutes} mins"

def list_running_containers():
    # Crear un cliente de Docker
    client = docker.from_env()

    # Obtener la lista de contenedores en ejecución
    containers = client.containers.list()

    # Imprimir información sobre cada contenedor
    print(f"{'ID':<12} {'Name':<30} {'Status':<10} {'Uptime':<12} {'CPU%':<8} {'MEM':<10} {'/MAX':<10} {'IOR/s':<8} {'IOW/s':<8} {'RX/s':<8} {'TX/s':<8} {'Command':<30}")
    print("="*80)

    for container in containers:
        container_id = container.id[:12]
        container_name = container.name
        container_status = container.status

        # Obtener detalles adicionales del contenedor
        stats = container.stats(stream=False)

        # Obtener la hora de inicio del contenedor
        started_at = container.attrs['State']['StartedAt']
        start_time = datetime.fromisoformat(started_at.replace("Z", "+00:00"))

        memory_usage = stats.get('memory_stats', {}).get('usage', 0)
        memory_limit = stats.get('memory_stats', {}).get('limit', 0)

        cpu_stats = stats.get('cpu_stats', {})
        cpu_usage = cpu_stats.get('cpu_usage', {}).get('total_usage', 0)
        system_cpu_usage = cpu_stats.get('system_cpu_usage', 0)

        # Evitar división por cero
        cpu_percent = (cpu_usage / system_cpu_usage * 100) if system_cpu_usage > 0 else 0

        io_stats = stats.get('io_stats', {})
        io_service_bytes_recursive = io_stats.get('io_service_bytes_recursive', [])
        io_read = io_service_bytes_recursive[0]['value'] if len(io_service_bytes_recursive) > 0 else 0
        io_write = io_service_bytes_recursive[1]['value'] if len(io_service_bytes_recursive) > 1 else 0

        networks = stats.get('networks', {})
        net_rx = networks.get('eth0', {}).get('rx_bytes', 0)
        net_tx = networks.get('eth0', {}).get('tx_bytes', 0)

        # Formatear el uso de memoria
        memory_usage_formatted = f"{memory_usage / (1024 * 1024):.2f} MB"
        memory_limit_formatted = f"{memory_limit / (1024 * 1024):.2f} MB"

        # Formatear IO y red
        io_read_per_sec = io_read / (1 if io_read == 0 else 1)  # Evitar división por cero
        io_write_per_sec = io_write / (1 if io_write == 0 else 1)
        net_rx_per_sec = net_rx / (1 if net_rx == 0 else 1)
        net_tx_per_sec = net_tx / (1 if net_tx == 0 else 1)

        container_command = container.attrs['Config']['Cmd']
        container_command_str = ' '.join(container_command)[:30]  # Mostrar solo los primeros 30 caracteres

        # Calcular y formatear el uptime
        uptime = format_uptime(start_time)

        # Convertir bytes a kilobytes y formatear a dos decimales
        net_rx_kb = net_rx_per_sec / 1024
        net_tx_kb = net_tx_per_sec / 1024

        print(f"{container_id:<12} {container_name:<30} {container_status:<10} {uptime:<12} {cpu_percent:<8.2f} {memory_usage_formatted:<10} {memory_limit_formatted:<10} {io_read_per_sec:<8.2f} {io_write_per_sec:<8.2f} {net_rx_kb:<8.2f}K {net_tx_kb:<8.2f}K {container_command_str:<30}")

if __name__ == "__main__":
    list_running_containers()
