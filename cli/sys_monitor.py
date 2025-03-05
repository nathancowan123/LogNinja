import psutil
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

def fetch_system_stats():
    """Fetches system statistics."""
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    temp = psutil.sensors_temperatures().get('cpu_thermal', [{}])[0].get('current', 'N/A')

    return cpu_usage, ram_usage, disk_usage, temp

def display_system_stats():
    """Displays live system statistics."""
    console.clear()
    console.print("[bold yellow]🖥 System Health Monitor[/bold yellow]\n")

    with Live(auto_refresh=True) as live:
        while True:
            cpu_usage, ram_usage, disk_usage, temp = fetch_system_stats()
            
            table = Table(title="System Stats", show_header=True, header_style="bold magenta")
            table.add_column("CPU Usage", justify="center", width=15)
            table.add_column("RAM Usage", justify="center", width=15)
            table.add_column("Disk Usage", justify="center", width=15)
            table.add_column("Temp (°C)", justify="center", width=15)

            table.add_row(f"{cpu_usage}%", f"{ram_usage}%", f"{disk_usage}%", f"{temp}°C")

            live.update(table)
            time.sleep(2)  # Refresh every 2 seconds

if __name__ == "__main__":
    display_system_stats()
