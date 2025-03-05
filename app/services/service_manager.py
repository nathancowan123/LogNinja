import threading
import time
import logging
from app.services.system_monitor import run_system_monitor
from app.services.log_db_handler import start_log_monitor
from app.services.docker_monitor import run_docker_monitor
from app.services.network_monitor import run_api_monitor

# ✅ Configure Logging
logger = logging.getLogger("main")

class ServiceManager:
    """Manages background services and ensures they restart if they crash."""

    def __init__(self):
        self.services = {
            "SystemMonitorThread": run_system_monitor,
            "LogMonitorThread": start_log_monitor,
            "DockerMonitorThread": run_docker_monitor,
            "APIMonitorThread": run_api_monitor,
        }

    def start_services(self):
        """Starts all services in separate threads."""
        for name, target in self.services.items():
            if not any(t.name == name for t in threading.enumerate()):
                thread = threading.Thread(target=target, daemon=True, name=name)
                thread.start()
                logger.info(f"✅ {name} started.")

    def monitor_services(self):
        """Continuously check if services are running, restart if crashed."""
        while True:
            for name, target in self.services.items():
                if not any(t.name == name for t in threading.enumerate()):
                    logger.warning(f"⚠️ {name} crashed! Restarting...")
                    thread = threading.Thread(target=target, daemon=True, name=name)
                    thread.start()
                    logger.info(f"✅ {name} restarted.")

            time.sleep(10)  # ✅ Adjust interval for performance

if __name__ == "__main__":
    manager = ServiceManager()
    manager.start_services()

    # ✅ Start monitoring thread
    monitor_thread = threading.Thread(target=manager.monitor_services, daemon=True, name="ServiceMonitorThread")
    monitor_thread.start()
