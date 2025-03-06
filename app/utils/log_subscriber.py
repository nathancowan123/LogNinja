import redis
import json
import time

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def start_log_subscriber():
    """Listens for logs from Redis and prints them to the console."""
    print("📡 Listening for live logs... (Press CTRL+C to stop)")
    pubsub = redis_client.pubsub()
    pubsub.subscribe("logninja_stream")  # ✅ Listen for log updates

    try:
        for message in pubsub.listen():
            if message["type"] == "message":
                log_data = json.loads(message["data"])
                timestamp = log_data.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))
                level = log_data.get("level", "INFO").upper()
                msg = log_data.get("message", "No message provided.")

                print(f"📝 [{timestamp}] [{level}] {msg}")

                # ✅ Specifically log CPU Temperature separately
                if "CPU Temp" in msg:
                    print(f"🔥 [{timestamp}] CPU Temperature Logged: {msg}")

    except Exception as e:
        print(f"❌ Log Subscriber Error: {e}")
        time.sleep(5)  # Prevent crash loops
        start_log_subscriber()  # Restart on failure

if __name__ == "__main__":
    start_log_subscriber()
