import sqlite3
import time
import psutil

DB_PATH = "/home/bruce/Projects/LogNinja-Core/db/logninja.db"

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
            net_recv INTEGER
        )
    """)
    conn.commit()
    conn.close()

def log_system_metrics():
    """Logs system metrics (CPU, RAM, Network) and checks for anomalies."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get current system metrics
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    net_io = psutil.net_io_counters()
    net_sent = net_io.bytes_sent
    net_recv = net_io.bytes_recv

    # Store data in SQLite
    cursor.execute(
        "INSERT INTO system_metrics (cpu, ram, net_sent, net_recv) VALUES (?, ?, ?, ?)",
        (cpu_usage, ram_usage, net_sent, net_recv)
    )
    conn.commit()

    # 🚧 Check for anomaly: CPU spike > 50% jump in 10 min window
    cursor.execute("SELECT avg(cpu) FROM system_metrics WHERE timestamp > DATETIME('now', '-10 minutes')")
    avg_cpu = cursor.fetchone()[0]

    if avg_cpu and cpu_usage > avg_cpu * 1.5:  # If current CPU is 50% above 10 min avg
        print(f"🚨 CPU Spike Detected! Current: {cpu_usage}% | Average: {avg_cpu:.2f}%")

    conn.close()

# ✅ Ensure the database is set up before starting logging
setup_database()

while True:
    log_system_metrics()
    time.sleep(10)  # Adjust interval as needed
