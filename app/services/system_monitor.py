import os
import psutil
import time
import redis
import json
import threading
from collections import deque

# 🚀 CONFIGURATION
CRITICAL_TEMP = 85  # Alert at 85°C
EMERGENCY_TEMP = 90  # Shutdown at 90°C
MONITOR_INTERVAL = 5  # System check every 5 sec
ANOMALY_HISTORY = 900  # Store last 15 min of data (900 sec)
CPU_THROTTLE_LIMIT = 85  # Throttle CPU if above 85%
RAM_THROTTLE_LIMIT = 90  # Free memory if above 90%

rebooting = False  # Prevent multiple reboots
running = True  # Flag for monitoring

# ✅ Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# ✅ Store historical system data for trend analysis
cpu_history = deque(maxlen=ANOMALY_HISTORY // MONITOR_INTERVAL)
temp_history = deque(maxlen=ANOMALY_HISTORY // MONITOR_INTERVAL)
ram_history = deque(maxlen=ANOMALY_HISTORY // MONITOR_INTERVAL)

def publish_log(level, message):
    """Publishes logs to Redis for real-time monitoring and immutable storage."""
    log_entry = {"level": level, "message": message, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    redis_client.rpush("logninja_logs", json.dumps(log_entry))
    redis_client.publish("logninja_stream", json.dumps(log_entry))

def get_cpu_temp():
    """Retrieve CPU temperature (Linux/macOS)."""
    try:
        temps = psutil.sensors_temperatures().get("coretemp", [])
        return temps[0].current if temps else -1
    except Exception:
        return -1

def throttle_system():
    """Dynamically reduce CPU priority and limit processes before reaching failure state."""
    publish_log("warning", "⚠️ Engaging auto-throttling mechanisms.")
    os.system("sudo cpufreq-set -g powersave")  # Reduce CPU frequency
    os.system("sudo renice -n 19 -p $(pgrep -d' ' python)")  # Lower priority of LogNinja process

def kill_high_usage_processes():
    """Find and kill high CPU or memory usage processes."""
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        if proc.info['cpu_percent'] > CPU_THROTTLE_LIMIT or proc.info['memory_percent'] > RAM_THROTTLE_LIMIT:
            publish_log("critical", f"❌ Killing process {proc.info['name']} (PID: {proc.info['pid']}) for excessive resource usage.")
            os.system(f"sudo kill -9 {proc.info['pid']}")

def emergency_shutdown():
    """Triggers an emergency safe shutdown if thresholds are exceeded."""
    global rebooting
    if not rebooting:
        rebooting = True
        publish_log("critical", "💀 EMERGENCY TEMP REACHED! Initiating shutdown...")
        os.system("reboot now")

def monitor_system():
    """Real-time anomaly detection & auto-recovery."""
    global running, rebooting
    while running:
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_temp = get_cpu_temp()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent

        cpu_history.append(cpu_usage)
        temp_history.append(cpu_temp)
        ram_history.append(ram_usage)

        publish_log("info", f"🔥 CPU: {cpu_usage}% | 🌡 Temp: {cpu_temp}°C | 💾 RAM: {ram_usage}% | 📂 Disk: {disk_usage}%")

        if len(cpu_history) >= 10:
            avg_cpu = sum(cpu_history) / len(cpu_history)
            avg_temp = sum(temp_history) / len(temp_history)
            avg_ram = sum(ram_history) / len(ram_history)

            if cpu_usage > avg_cpu * 1.5:
                publish_log("warning", f"🚨 CPU Spike! Current: {cpu_usage}% | 15-min Avg: {avg_cpu:.2f}%")
            if ram_usage > avg_ram * 1.5:
                publish_log("warning", f"🚨 RAM Spike! Current: {ram_usage}% | 15-min Avg: {avg_ram:.2f}%")
            if cpu_temp > avg_temp * 1.3:
                publish_log("warning", f"🔥 Temp Spike! Current: {cpu_temp}°C | 15-min Avg: {avg_temp:.2f}°C")

        if cpu_usage > CPU_THROTTLE_LIMIT:
            publish_log("warning", "🚨 High CPU Usage! Activating auto-throttling...")
            throttle_system()
            kill_high_usage_processes()
        if ram_usage > RAM_THROTTLE_LIMIT:
            publish_log("warning", "🚨 High RAM Usage! Freeing up memory and killing processes...")
            os.system("sync; echo 3 > /proc/sys/vm/drop_caches")
            kill_high_usage_processes()
        if cpu_temp >= CRITICAL_TEMP:
            publish_log("critical", f"⚠️ CPU Temp Critical at {cpu_temp}°C! Stopping non-essential services...")
            os.system("sudo systemctl stop non_essential_services")
        if cpu_temp >= EMERGENCY_TEMP:
            emergency_shutdown()

        time.sleep(MONITOR_INTERVAL)

def start_monitoring():
    """Starts system monitoring in a separate thread."""
    publish_log("info", "🚀 LogNinja System Monitoring Started!")
    monitoring_thread = threading.Thread(target=monitor_system, daemon=True)
    monitoring_thread.start()

if __name__ == "__main__":
    start_monitoring()