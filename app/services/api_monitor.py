import logging
import time
import threading
from app.utils.logger import log_message
from app.services.api_checker import check_api_rate_limits  # ✅ Ensure import

logger = logging.getLogger("LogNinja")

_api_monitor_started = False  # ✅ Prevent duplicate monitoring
_api_monitor_lock = threading.Lock()  # ✅ Prevent concurrent executions

def run_api_monitor():
    """Continuously monitors API usage and logs rate limits."""
    global _api_monitor_started

    with _api_monitor_lock:
        if _api_monitor_started:
            logger.debug("⚠️ API Monitoring is already running. Skipping duplicate startup.")
            return

        _api_monitor_started = True
        logger.info("🚀 API Monitoring Initialized!")

    while _api_monitor_started:  # ✅ Allows stopping the thread safely
        try:
            logger.debug("🔄 Checking API Rate Limits...")  # ✅ Debug log

            api_name = "ExampleAPI"
            max_requests = 10000  # ✅ Replace with actual API quota
            used_requests = 850   # ✅ Replace with real API data

            check_api_rate_limits(api_name, max_requests, used_requests)

            logger.debug(f"✅ API {api_name} checked: {used_requests}/{max_requests} used")

        except Exception as e:
            log_message(f"❌ API Monitoring Error: {str(e)}", "error")

        time.sleep(30)  # ✅ Set a **longer interval** (default: 30 sec)

# ✅ Start API Monitor in a background thread (Prevents blocking main thread)
def start_api_monitor():
    """Ensures API monitoring runs in a single background thread."""
    if any(thread.name == "APIMonitorThread" for thread in threading.enumerate()):
        logger.info("⚠️ API Monitor is already running. Skipping duplicate startup.")
        return

    api_thread = threading.Thread(target=run_api_monitor, daemon=True, name="APIMonitorThread")
    api_thread.start()
    logger.info("🚀 API Monitoring Started Successfully!")