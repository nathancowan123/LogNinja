import docker
import threading
import os
import time
import redis
import json
import subprocess
from app.utils.logger import log_message

# ✅ Persistent Set to Track Logged Containers
_seen_containers = set()
docker_monitor_lock = threading.Lock()

# ✅ Redis Connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def publish_docker_event(event_type, message):
    """Publishes Docker events to Redis for real-time monitoring."""
    log_entry = {"event": event_type, "message": message, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    redis_client.rpush("logninja_docker_logs", json.dumps(log_entry))  # ✅ Store in Redis list
    redis_client.publish("logninja_docker_stream", json.dumps(log_entry))  # ✅ Publish for live updates

def check_docker_status():
    """Monitor Docker containers and detect changes."""
    with docker_monitor_lock:  # Prevent concurrent access
        try:
            client = docker.from_env()
            running_containers = client.containers.list()
            current_ids = {c.short_id for c in running_containers}

            if not running_containers:
                log_message("🚨 No active Docker containers found!", "error")
                publish_docker_event("error", "🚨 No active Docker containers found!")

            # ✅ Log newly started containers
            for container in running_containers:
                if container.short_id not in _seen_containers:
                    log_message(f"✅ Docker Running: {container.name} (ID: {container.short_id})", "info")
                    publish_docker_event("info", f"✅ Docker Running: {container.name} (ID: {container.short_id})")

            # ✅ Log stopped containers
            for stopped_id in _seen_containers - current_ids:
                log_message(f"🛑 Docker Container stopped (ID: {stopped_id})", "warning")
                publish_docker_event("warning", f"🛑 Docker Container stopped (ID: {stopped_id})")

            # ✅ Update the tracked set for next cycle
            _seen_containers.clear()
            _seen_containers.update(current_ids)

        except Exception as e:
            log_message(f"❌ Docker Monitoring Failed: {str(e)}", "error")
            publish_docker_event("error", f"❌ Docker Monitoring Failed: {str(e)}")

def get_docker_status():
    """Fetch running Docker containers and store results in Redis."""
    try:
        result = subprocess.run(["docker", "ps", "--format", "{{.Names}} {{.Status}}"],
                                stdout=subprocess.PIPE, text=True)
        containers = [line.split(" ", 1) for line in result.stdout.strip().split("\n") if line]

        redis_client.set("logninja_docker", json.dumps(containers))  # ✅ Store in Redis for retrieval
        publish_docker_event("info", "🔍 Docker status updated in Redis")  # ✅ Log status update
    except Exception as e:
        redis_client.set("logninja_docker", json.dumps({"error": str(e)}))
        publish_docker_event("error", f"❌ Failed to fetch Docker status: {str(e)}")

def run_docker_monitor():
    """Run Docker monitoring process once per cycle."""
    check_docker_status()
    get_docker_status()
