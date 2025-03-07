import redis
import json
import time
import re

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def extract_temp(message):
    """Extracts numeric temperature from a message string."""
    match = re.search(r"(\d+(\.\d+)?)°C", message)
    if match:
        return float(match.group(1))  # ✅ Extracts numeric value
    return None  # ✅ Returns None if no match

def start_log_subscriber():
    """Listens for logs from Redis and prints them to the console."""
    print("📡 Listening for live logs & alerts... (Press CTRL+C to stop)")
    pubsub = redis_client.pubsub()
    pubsub.subscribe("logninja_stream")  # ✅ Listen for log updates

    try:
        for message in pubsub.listen():
            if message["type"] == "message":
                log_data = json.loads(message["data"])
                timestamp = log_data.get("timestamp", time.strftime("%Y-%m-%d %H:%M:%S"))
                level = log_data.get("level", "INFO").upper()
                msg = log_data.get("message", "No message provided.")

                # ✅ Extract CPU temp safely
                temp_value = extract_temp(msg)
                if temp_value is not None:
                    print(f"🔥 [{timestamp}] [CPU TEMP] {msg} (Parsed Temp: {temp_value}°C)")

                    # ✅ **React to Critical Temperature**
                    if temp_value >= 95:
                        print(f"🚨 CRITICAL: CPU TEMP TOO HIGH ({temp_value}°C)! Consider throttling or shutdown.")
                        redis_client.publish("logninja_alert_stream", json.dumps({"alert": f"Critical CPU Temp: {temp_value}°C"}))

                else:
                    print(f"📝 [{timestamp}] [{level}] {msg}")

    except Exception as e:
        print(f"❌ Log Subscriber Error: {e}")
        time.sleep(5)  # Prevent crash loops
        start_log_subscriber()  # Restart on failure

if __name__ == "__main__":
    start_log_subscriber()
