import psutil
import time
import logging
import threading
import redis
import json
import sqlite3
import os

# ✅ Configure logging
logging.basicConfig(filename="/home/bruce/Projects/LogNinja-Core/logs/network.log", level=logging.WARNING)

# ✅ Redis Connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# ✅ SQLite Database Path
DB_PATH = "/home/bruce/Projects/LogNinja-Core/db/logninja.db"

class NetworkMonitor:
    def __init__(self):
        self.prev_sent = psutil.net_io_counters().bytes_sent
        self.prev_recv = psutil.net_io_counters().bytes_recv
        self.last_check_time = time.time()  # Track time for speed calculations
        self.setup_database()  # ✅ Ensure DB is ready

    def setup_database(self):
        """Ensure the network_metrics table exists before logging data."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS network_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT (DATETIME('now')),
                upload_speed REAL,
                download_speed REAL,
                total_sent INTEGER,
                total_received INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def convert_bytes(self, bytes_value):
        """Converts bytes to human-readable MB/GB format."""
        if bytes_value < 1_000_000:
            return f"{bytes_value / 1_000:.2f} KB"
        elif bytes_value < 1_000_000_000:
            return f"{bytes_value / 1_000_000:.2f} MB"
        else:
            return f"{bytes_value / 1_000_000_000:.2f} GB"

    def publish_network_event(self, event_type, message):
        """Publishes network events to Redis for real-time monitoring."""
        log_entry = {
            "event": event_type,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        redis_client.rpush("logninja_network_logs", json.dumps(log_entry))  # ✅ Store logs in Redis
        redis_client.publish("logninja_network_stream", json.dumps(log_entry))  # ✅ Publish for live updates

    def log_to_database(self, upload_speed, download_speed, total_sent, total_received):
        """Stores network data in SQLite for historical analysis."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO network_metrics (upload_speed, download_speed, total_sent, total_received) VALUES (?, ?, ?, ?)",
            (upload_speed, download_speed, total_sent, total_received)
        )
        conn.commit()
        conn.close()

    def check_network_spike(self):
        """Monitors network traffic for sudden spikes and saves stats."""
        net_io = psutil.net_io_counters()
        current_time = time.time()
        elapsed_time = current_time - self.last_check_time  # Time since last check

        sent_diff = net_io.bytes_sent - self.prev_sent
        recv_diff = net_io.bytes_recv - self.prev_recv
        sent_speed = sent_diff / elapsed_time  # Speed in bytes/sec
        recv_speed = recv_diff / elapsed_time

        # ✅ Convert speeds to Mbps for better readability
        sent_speed_mbps = (sent_speed * 8) / 1_000_000
        recv_speed_mbps = (recv_speed * 8) / 1_000_000

        self.prev_sent = net_io.bytes_sent
        self.prev_recv = net_io.bytes_recv
        self.last_check_time = current_time  # ✅ Update timestamp

        # ✅ Store in Redis
        usage_msg = f"📡 Network Speed: Upload: {sent_speed_mbps:.2f} Mbps | Download: {recv_speed_mbps:.2f} Mbps"
        self.publish_network_event("info", usage_msg)

        # ✅ Save to SQLite
        self.log_to_database(sent_speed_mbps, recv_speed_mbps, net_io.bytes_sent, net_io.bytes_recv)

        # ✅ Detect spike (10MB+ change in 10 sec)
        if sent_diff > 10_000_000 or recv_diff > 10_000_000:
            alert_msg = f"🚨 Network Spike! Upload: {self.convert_bytes(sent_diff)}, Download: {self.convert_bytes(recv_diff)}"
            logging.warning(alert_msg)
            self.publish_network_event("warning", alert_msg)  # ✅ Send alert to Redis

    def run_monitor(self):
        """Runs network monitoring in a loop."""
        while True:
            self.check_network_spike()
            time.sleep(10)  # ✅ Adjust interval as needed

# ✅ Ensure `api_monitor.py` is only imported **inside** the function
def start_network_monitor():
    from app.services.api_monitor import start_api_monitor  # ✅ Moved import inside function

    network_monitor = NetworkMonitor()
    monitor_thread = threading.Thread(target=network_monitor.run_monitor, daemon=True, name="NetworkMonitorThread")
    monitor_thread.start()
    
    start_api_monitor()  # ✅ Start API monitor after network monitor starts
