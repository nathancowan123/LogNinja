# 🛠 What Does It Do?
# Test	Action	Expected LogNinja Response
# CPU Stress	Overloads all CPU cores	🔥 Logs CPU % and warns if over 90%
# RAM Stress	Uses 80% of RAM	🚨 Alerts on high RAM usage
# Disk I/O Stress	Writes & deletes large files	📂 Monitors disk space & alerts if critical
# Live Monitoring	Logs CPU, RAM, Disk every second	✅ Shows trends in LogNinja
# Auto-Stop	Runs for 30s, then stops	✅ Releases resources

import os
import psutil
import time
import threading
import redis
import json

# ✅ Redis Connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

running = True  # Flag to stop stress tests

def publish_log(level, message):
    """Send logs to LogNinja for real-time monitoring."""
    log_entry = {"level": level, "message": message, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    redis_client.rpush("logninja_logs", json.dumps(log_entry))
    redis_client.publish("logninja_stream", json.dumps(log_entry))

# ✅ CPU Stress Function (All Cores)
def cpu_stress():
    while running:
        _ = [x**2 for x in range(10**6)]  # Heavy CPU computation

# ✅ RAM Stress Function (~80% of Available RAM)
def memory_stress():
    global memory_hog
    total_memory = psutil.virtual_memory().total
    target_memory = int(total_memory * 0.8)
    memory_hog = bytearray(target_memory)
    publish_log("warning", "🚨 RAM Stress Test Running! 80% Memory Usage")

# ✅ Disk I/O Stress Function (Large File Writes)
def disk_stress():
    temp_file = "/tmp/logninja_stresstest.tmp"
    with open(temp_file, "w") as f:
        for _ in range(10000):
            f.write("LogNinja Stress Test " * 100 + "\n")
    os.remove(temp_file)
    publish_log("warning", "🚨 Disk Stress Test Completed!")

# ✅ Monitor System During Stress Test
def monitor_system():
    start_time = time.time()
    while time.time() - start_time < 30:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent

        publish_log("info", f"🔥 CPU: {cpu_usage}% | 💾 RAM: {ram_usage}% | 📂 Disk: {disk_usage}%")
        time.sleep(1)

# ✅ Stop Stress Test
def stop_stress_test():
    global running, memory_hog
    running = False
    memory_hog = None  # Release memory
    publish_log("info", "✅ System Overload Test Stopped! Resources Released!")

# ✅ Start the Stress Test
if __name__ == "__main__":
    publish_log("info", "🚀 Starting 30-second Extreme System Overload Test!")

    running = True
    cpu_threads = [threading.Thread(target=cpu_stress) for _ in range(os.cpu_count())]
    memory_thread = threading.Thread(target=memory_stress)
    disk_thread = threading.Thread(target=disk_stress)
    monitor_thread = threading.Thread(target=monitor_system)

    for t in cpu_threads:
        t.start()
    memory_thread.start()
    disk_thread.start()
    monitor_thread.start()

    time.sleep(30)  # ✅ Run for 30 seconds

    stop_stress_test()  # ✅ Stop the test

    for t in cpu_threads:
        t.join()
    memory_thread.join()
    disk_thread.join()
    monitor_thread.join()

    publish_log("info", "✅ Test Complete! System should return to normal.")
