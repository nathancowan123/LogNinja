import redis
import json

# ✅ Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def listen_for_logs():
    """Subscribes to Redis Pub/Sub and prints new logs in real-time."""
    pubsub = redis_client.pubsub()
    pubsub.subscribe("logninja_stream")  # ✅ Listen to log events

    print("📡 Listening for live logs... (Press CTRL+C to stop)")
    
    for message in pubsub.listen():
        if message["type"] == "message":
            log_entry = json.loads(message["data"])
            print(f"📝 [{log_entry['level']}] {log_entry['message']}")

if __name__ == "__main__":
    listen_for_logs()
