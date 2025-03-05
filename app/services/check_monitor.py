import time
import logging
import threading

# ✅ Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TestMonitor")

# ✅ Global thread tracker
monitor_thread = None  

def test_monitor():
    """🚀 Safe test loop that logs system status every 30 seconds."""
    while True:
        logger.info("🔍 Test Monitor Running... System is OK.")
        time.sleep(30)  # ✅ Runs every 30 seconds

def start_test_monitor():
    """✅ Ensures only ONE instance of test_monitor is running."""
    global monitor_thread
    if monitor_thread and monitor_thread.is_alive():
        logger.info("⚠️ Test Monitor already running. Preventing duplicate instances.")
        return  # Stops multiple threads from running

    monitor_thread = threading.Thread(target=test_monitor, daemon=True)
    monitor_thread.start()
    logger.info("🚀 Test Monitor Started!")

# ✅ Start the test
if __name__ == "__main__":
    start_test_monitor()

    # ✅ Keep the script running to observe logs
    while True:
        time.sleep(1)
