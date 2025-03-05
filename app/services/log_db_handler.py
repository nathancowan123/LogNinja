import sqlite3
import time
import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_DIR = "logs/"
DB_PATH = "db/logninja.db"

LOG_TABLES = {
    "logninja.log": "main_logs",
    "errors.log": "errors",
    "ratelimits.log": "ratelimits",
    "unauthorized.log": "unauthorized"
}

class LogHandler(FileSystemEventHandler):
    """Handles log file changes and inserts them into SQLite3."""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.last_positions = {log: 0 for log in LOG_TABLES}  # Track file positions
        self.setup_db()

    def setup_db(self):
        """Creates tables for each log category."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for table in LOG_TABLES.values():
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    level TEXT,
                    source TEXT,
                    message TEXT
                )
            """)
        conn.commit()
        conn.close()

    def process_log_entry(self, log_file, entry):
        """Parses log entry and stores it in SQLite."""
        try:
            parts = entry.strip().split(" ", 3)
            if len(parts) < 4:
                return  # Ignore malformed logs

            timestamp, source, level, message = parts
            table = LOG_TABLES.get(log_file, "main_logs")

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table} (timestamp, source, level, message) VALUES (?, ?, ?, ?)", 
                           (timestamp, source, level, message))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Error processing log: {e}")

    def on_modified(self, event):
        """Triggered when log files are updated."""
        log_file = os.path.basename(event.src_path)
        if log_file in LOG_TABLES:
            with open(event.src_path, "r") as file:
                file.seek(self.last_positions[log_file])
                for line in file:
                    self.process_log_entry(log_file, line)
                self.last_positions[log_file] = file.tell()  # Update read position

def start_log_monitor():
    """Starts log monitoring in a background thread."""
    event_handler = LogHandler(DB_PATH)
    observer = Observer()
    observer.schedule(event_handler, path=LOG_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(2)  # Polling interval
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
