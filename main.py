import logging
import logging.config
import yaml
import os
import threading
from app import create_app
from app.services.ninja import start_ninja_log_cleanup  # ✅ Log Cleanup

# ✅ Load Logging Configuration from YAML (if available)
log_config_path = "config/logging.yaml"
if os.path.exists(log_config_path):
    with open(log_config_path, "r") as file:
        config = yaml.safe_load(file)
        logging.config.dictConfig(config)

logger = logging.getLogger("LogNinja")
logger.info("✅ LogNinja Logging Initialized!")

# ✅ Initialize Flask App
app = create_app()
logger.info("🚀 Flask App Started Successfully!")

# ✅ Delayed Import to Avoid Circular Dependency
def start_monitoring_services():
    """Ensures all monitoring services start safely without duplicates."""
    from app.services.api_monitor import start_api_monitor
    from app.services.network_monitor import start_network_monitor
    from app.services.system_monitor import start_monitoring  # ✅ Fixed missing import

    monitoring_threads = [
        ("ApiMonitorThread", start_api_monitor),
        ("NetworkMonitorThread", start_network_monitor),
        ("SystemMonitorThread", start_monitoring)
    ]

    for thread_name, func in monitoring_threads:
        if any(thread.name == thread_name for thread in threading.enumerate()):
            logger.info(f"⚠️ {thread_name} is already running. Skipping duplicate startup.")
        else:
            try:
                monitor_thread = threading.Thread(target=func, daemon=True, name=thread_name)
                monitor_thread.start()
                logger.info(f"🚀 {thread_name} Started Successfully!")
            except Exception as e:
                logger.error(f"❌ Failed to start {thread_name}: {str(e)}")

if __name__ == "__main__":
    logger.info("🚀 Starting LogNinja Services...")

    start_ninja_log_cleanup()  # ✅ Ensures log cleanup runs only once
    start_monitoring_services()  # ✅ Starts API, Network & System monitoring

    logger.info("🚀 LogNinja Monitoring Services are Running!")

    # ✅ Prevent Flask from restarting and duplicating threads
    app.run(host="0.0.0.0", port=8100, debug=False, use_reloader=False)
