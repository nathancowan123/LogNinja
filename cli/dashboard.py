import os
import sys
import time
import sqlite3
import threading
from rich.console import Console
from rich.table import Table
from rich.live import Live
from logs_viewer import display_logs
from sys_monitor import display_system_stats
from api_monitor import display_api_stats

console = Console()

def show_dashboard():
    """Displays an interactive CLI dashboard with multiple monitoring views."""
    while True:
        console.clear()
        console.print("[bold cyan]🚀 LogNinja CLI Dashboard[/bold cyan]\n")
        
        # Create a tabbed interface
        table = Table(title="📊 Dashboard", show_header=True, header_style="bold magenta")
        table.add_column("1️⃣ Logs", justify="center", style="cyan", no_wrap=True)
        table.add_column("2️⃣ System Stats", justify="center", style="yellow", no_wrap=True)
        table.add_column("3️⃣ API Monitor", justify="center", style="green", no_wrap=True)
        
        table.add_row("View log entries", "Check CPU, RAM, Disk", "Monitor API rate limits")

        console.print(table)
        choice = console.input("\n[bold white]Choose an option (1-3) or (Q)uit: [/bold white]").strip().lower()
        
        if choice == "1":
            display_logs()
        elif choice == "2":
            display_system_stats()
        elif choice == "3":
            display_api_stats()
        elif choice == "q":
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit()
        else:
            console.print("[bold yellow]Invalid choice! Try again.[/bold yellow]")

        time.sleep(1)

if __name__ == "__main__":
    show_dashboard()
