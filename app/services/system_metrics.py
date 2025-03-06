import os
import psutil
import time
import redis
import json
import threading
import subprocess
from app.utils.logger import log_message
from app.services.docker_monitor import run_docker_monitor
from app.services.api_monitor import run_api_monitor  # ✅ Fixed import

# 🚀 CONFIGURATION
CRITICAL_TEMP = 85  # Logging threshold
EMERGENCY_TEMP = 101  # Immediate reboot threshold
MONITOR_INTERVAL = 10  # Check system every X seconds
SHUTDOWN_DELAY = 15  # Seconds before reboot after hitting CRITICAL_TEMP
rebooting = False  # Prevent multiple reboots

# ✅ Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def publish_log(level, message):
    """Publishes logs to Redis for real-time monitoring and stores in history."""
    log_entry = {"level": level, "message": message, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    redis_client.rpush("logninja_logs", json.dumps(log_entry))  # Store in Redis list
    redis_client.publish("logninja_stream", json.dumps(log_entry))  # Publish to Pub/Sub

def get_cpu_temp():
    """Retrieve CPU temperature (Linux/macOS)."""
    try:
        temps = psutil.sensors_temperatures().get("coretemp", [])
        return temps[0].current if temps else -1
    except Exception:
        return -1

def check_cpu_status():
    """Monitor CPU usage and temperature, triggering actions if necessary."""
    global rebooting
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_temp = get_cpu_temp()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    publish_log("info", f"[{timestamp}] 🖥 CPU Usage: {cpu_usage}%")
    publish_log("info", f"[{timestamp}] 🌡 CPU Temp: {cpu_temp}°C")

    if cpu_usage > 80:
        publish_log("warning", f"[{timestamp}] 🔥 High CPU Usage Detected: {cpu_usage}%")

    if cpu_temp >= CRITICAL_TEMP:
        publish_log("warning", f"[{timestamp}] ⚠️ Warning: CPU Temperature High at {cpu_temp}°C!")

    if cpu_temp >= EMERGENCY_TEMP and not rebooting:
        rebooting = True
        publish_log("critical", f"[{timestamp}] 💀 EMERGENCY TEMP {cpu_temp}°C REACHED! Rebooting immediately!")
        os.system("reboot now")
        return

def check_memory_status():
    """Monitor memory usage and detect high RAM usage or swap reliance."""
    memory_info = psutil.virtual_memory()
    swap_info = psutil.swap_memory()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    publish_log("info", f"[{timestamp}] 💾 RAM Usage: {memory_info.percent}% ({memory_info.available // (1024 * 1024)} MB Free)")
    publish_log("info", f"[{timestamp}] 🔄 Swap Usage: {swap_info.percent}% ({swap_info.free // (1024 * 1024)} MB Free)")

    if memory_info.percent > 85:
        publish_log("warning", f"[{timestamp}] 🚨 High Memory Usage: {memory_info.percent}% used!")
    if swap_info.percent > 50:
        publish_log("warning", f"[{timestamp}] ⚠️ High Swap Usage: {swap_info.percent}% used!")

def check_disk_status():
    """Monitor disk usage and detect critical storage issues."""
    disk_usage = psutil.disk_usage('/')
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    publish_log("info", f"[{timestamp}] 🗄 Disk Usage: {disk_usage.percent}% ({disk_usage.free // (1024 * 1024 * 1024)} GB Free)")

    if disk_usage.percent > 90:
        publish_log("warning", f"[{timestamp}] 🚨 Low Disk Space: {disk_usage.percent}% used!")

def run_system_monitor():
    """Run the core system monitoring process in a loop."""
    publish_log("info", "🚀 System Monitor Started!")
    while True:
        check_cpu_status()
        check_memory_status()
        check_disk_status()
        run_docker_monitor()  # ✅ Logs running Docker containers
        run_api_monitor()  # ✅ Logs API activity
        time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    run_system_monitor()
