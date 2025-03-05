import docker
import threading
from app.utils.logger import log_message

# ✅ Persistent Set to Track Logged Containers
_seen_containers = set()
docker_monitor_lock = threading.Lock()

def check_docker_status():
    """Monitor Docker containers and detect changes."""
    with docker_monitor_lock:  # Prevent concurrent access
        try:
            client = docker.from_env()
            running_containers = client.containers.list()
            current_ids = {c.short_id for c in running_containers}

            if not running_containers:
                log_message("🚨 No active Docker containers found!", "error")

            # ✅ Log newly started containers
            for container in running_containers:
                if container.short_id not in _seen_containers:
                    log_message(f"✅ Docker Running: {container.name} (ID: {container.short_id})", "info")

            # ✅ Log stopped containers
            for stopped_id in _seen_containers - current_ids:
                log_message(f"🛑 Docker Container stopped (ID: {stopped_id})", "warning")

            # ✅ Update the tracked set for next cycle
            _seen_containers.clear()
            _seen_containers.update(current_ids)

        except Exception as e:
            log_message(f"❌ Docker Monitoring Failed: {str(e)}", "error")

def run_docker_monitor():
    """Run Docker monitoring process once per cycle."""
    check_docker_status()
