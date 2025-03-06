import redis
import sqlite3
import json

# Connect to Redis and SQLite
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
DB_PATH = "db/logninja.db"

def store_log(entry):
    """Insert logs from Redis into SQLite"""
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

    cursor.execute("INSERT INTO logs (level, message) VALUES (?, ?)", 
                   (entry["level"], entry["message"]))
    
    conn.commit()
    conn.close()

def process_logs():
    """Continuously fetch logs from Redis and store them in SQLite"""
    while True:
        log_data = redis_client.lpop("logninja_logs")  # Fetch the oldest log
        if log_data:
            log_entry = json.loads(log_data)
            store_log(log_entry)

if __name__ == "__main__":
    print("🛠️ Log worker started...")
    process_logs()
