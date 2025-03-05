import sqlite3
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live

DB_PATH = "../db/logninja.db"
console = Console()

def fetch_logs(limit=10):
    """Fetches the latest logs from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, source, level, message FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    logs = cursor.fetchall()
    conn.close()
    return logs

def display_logs():
    """Displays logs in a live table."""
    console.clear()
    console.print("[bold cyan]📜 Log Viewer[/bold cyan]\n")

    with Live(auto_refresh=True) as live:
        while True:
            table = Table(title="Recent Logs", show_header=True, header_style="bold magenta")
            table.add_column("Timestamp", style="dim", width=20)
            table.add_column("Source", width=15)
            table.add_column("Level", width=10)
            table.add_column("Message", width=50, overflow="fold")

            logs = fetch_logs(10)
            for log in logs:
                table.add_row(*log)

            live.update(table)
            time.sleep(2)  # Refresh logs every 2 seconds

if __name__ == "__main__":
    display_logs()
