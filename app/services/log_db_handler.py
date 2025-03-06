import redis
import sqlite3
import json
import time
import threading

# ✅ Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# ✅ SQLite Database Path
DB_PATH = "db/logninja.db"

def setup_database():
    """Creates the logs table in SQLite if it doesn't already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            level TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()

def store_logs():
    """Continuously fetch logs from Redis and store them in SQLite."""
    while True:
        log_data = redis_client.lpop("logninja_logs")  # Fetch the oldest log
        if log_data:
            log_entry = json.loads(log_data)

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs (level, message) VALUES (?, ?)", 
                           (log_entry["level"], log_entry["message"]))
            conn.commit()
            conn.close()
        
        time.sleep(2)  # ✅ Fetch logs every 2 seconds to prevent high CPU usage

# ✅ Only setup database once
setup_database()
