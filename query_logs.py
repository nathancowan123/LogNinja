import sqlite3

DB_PATH = "db/logninja.db"

def fetch_latest_logs(limit=10):
    """Fetch the latest logs from the SQLite3 database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    logs = cursor.fetchall()
    
    conn.close()
    return logs

if __name__ == "__main__":
    latest_logs = fetch_latest_logs()
    for log in latest_logs:
        print(log)
