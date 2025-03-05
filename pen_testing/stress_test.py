import time
import threading
import logging
import psutil
import os

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("LogNinja")

# ✅ CPU Stress Function (Runs on multiple threads)
def cpu_stress():
    while running:
        _ = [x**2 for x in range(10**6)]  # Heavy CPU computation

# ✅ RAM Stress Function (Consumes ~80% of available RAM)
def memory_stress():
    global memory_hog
    total_memory = psutil.virtual_memory().total
    target_memory = int(total_memory * 0.8)  # Use 80% of RAM
    memory_hog = bytearray(target_memory)  # Allocate memory

# ✅ Disk I/O Stress Function (Writes and Deletes Temporary Files)
def disk_stress():
    temp_file = "/tmp/logninja_stresstest.tmp"
    with open(temp_file, "w") as f:
        for _ in range(10000):  # Large writes
            f.write("LogNinja Stress Test " * 100 + "\n")
    os.remove(temp_file)  # Cleanup

# ✅ System Monitor (Logs CPU, RAM, Disk Usage)
def monitor_system():
    start_time = time.time()
    while time.time() - start_time < 30:  # Run for 30 seconds
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent
        logger.info(f"🔥 CPU: {cpu_usage}% | 💾 RAM: {ram_usage}% | 📂 Disk: {disk_usage}%")
        time.sleep(1)

# ✅ Start the test
if __name__ == "__main__":
    logger.info("🚀 Starting 30-second Extreme System Overload Test!")

    running = True
    cpu_threads = [threading.Thread(target=cpu_stress) for _ in range(os.cpu_count())]  # One thread per core
    memory_thread = threading.Thread(target=memory_stress)
    disk_thread = threading.Thread(target=disk_stress)
    monitor_thread = threading.Thread(target=monitor_system)

    # ✅ Start all threads
    for t in cpu_threads:
        t.start()
    memory_thread.start()
    disk_thread.start()
    monitor_thread.start()

    # ✅ Wait for 30 seconds
    time.sleep(30)

    # ✅ Stop the test
    running = False
    memory_hog = None  # Release memory
    logger.info("✅ Test Complete! System should return to normal.")

    # ✅ Wait for all threads to exit
    for t in cpu_threads:
        t.join()
    memory_thread.join()
    disk_thread.join()
    monitor_thread.join()
