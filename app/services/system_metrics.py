import sqlite3
import time
import psutil
import redis
import json
import os

DB_PATH = "/home/bruce/Projects/LogNinja-Core/db/logninja.db"

# ✅ Redis Connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def setup_database():
    """Ensures the system_metrics table exists before logging data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT (DATETIME('now')),
            cpu REAL,
            ram REAL,
            net_sent INTEGER,
            net_recv INTEGER,
            disk_usage REAL,
            disk_free INTEGER,
            hostname TEXT,
            uptime INTEGER,
            load_avg REAL,
            cpu_temp REAL
        )
    """)
    conn.commit()
    conn.close()

def get_system_uptime():
    """Returns system uptime in seconds."""
    return int(time.time() - psutil.boot_time())

def get_load_average():
    """Returns the system's 1-minute load average."""
    return os.getloadavg()[0]

def get_cpu_temp():
    """Retrieve CPU temperature (Linux/macOS)."""
    try:
        temps = psutil.sensors_temperatures().get("coretemp", [])
        return temps[0].current if temps else -1
    except Exception:
        return -1

def log_system_metrics():
    """Logs system metrics and stores in SQLite & Redis."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ✅ Get system metrics
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    net_io = psutil.net_io_counters()
    net_sent = net_io.bytes_sent
    net_recv = net_io.bytes_recv
    disk_usage = psutil.disk_usage("/").percent
    disk_free = psutil.disk_usage("/").free // (1024 * 1024 * 1024)  # Convert to GB
    hostname = os.uname().nodename
    uptime = get_system_uptime()
    load_avg = get_load_average()
    cpu_temp = get_cpu_temp()

    # ✅ Store data in SQLite
    cursor.execute(
        "INSERT INTO system_metrics (cpu, ram, net_sent, net_recv, disk_usage, disk_free, hostname, uptime, load_avg, cpu_temp) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (cpu_usage, ram_usage, net_sent, net_recv, disk_usage, disk_free, hostname, uptime, load_avg, cpu_temp)
    )
    conn.commit()

    # ✅ Store real-time metrics in Redis
    redis_client.set("logninja_system_metrics", json.dumps({
        "cpu": cpu_usage,
        "ram": ram_usage,
        "disk_usage": disk_usage,
        "cpu_temp": cpu_temp,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }))

    conn.close()

def start_logging():
    """Initializes the database and starts the logging loop."""
    setup_database()
    while True:
        log_system_metrics()
        time.sleep(15)  # Logs every 15 seconds

if __name__ == "__main__":
    start_logging()
