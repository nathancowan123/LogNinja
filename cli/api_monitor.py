import random
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

def fetch_api_stats():
    """Simulates fetching API rate usage."""
    usage = random.randint(60, 95)  # Simulated API usage percentage
    return usage

def display_api_stats():
    """Displays live API monitoring table."""
    console.clear()
    console.print("[bold green]📡 API Monitor[/bold green]\n")

    with Live(auto_refresh=True) as live:
        while True:
            usage = fetch_api_stats()

            table = Table(title="API Rate Limit Usage", show_header=True, header_style="bold magenta")
            table.add_column("API Name", justify="center", width=20)
            table.add_column("Usage", justify="center", width=15)
            table.add_column("Status", justify="center", width=20)

            status = "✅ OK" if usage < 80 else "⚠️ Warning" if usage < 90 else "🔥 Critical"

            table.add_row("ExampleAPI", f"{usage}%", status)

            live.update(table)
            time.sleep(2)  # Refresh every 2 seconds

if __name__ == "__main__":
    display_api_stats()
