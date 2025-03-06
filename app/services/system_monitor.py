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

def get_system_uptime():
    """Returns system uptime in seconds."""
    return int(time.time() - psutil.boot_time())

def get_load_average():
    """Returns the system's 1-minute load average."""
    return os.getloadavg()[0]

def check_cpu_status():
    """Monitor CPU usage and detect high usage conditions."""
    cpu_usage = psutil.cpu_percent(interval=1)
    publish_log("info", f"🖥 CPU Usage: {cpu_usage}%")
    if cpu_usage > 80:
        publish_log("warning", f"🔥 High CPU Usage Detected: {cpu_usage}%")

def check_memory_status():
    """Monitor memory usage and detect high RAM usage or swap reliance."""
    memory_info = psutil.virtual_memory()
    swap_info = psutil.swap_memory()
    publish_log("info", f"💾 RAM Usage: {memory_info.percent}% ({memory_info.available // (1024 * 1024)} MB Free)")
    publish_log("info", f"🔄 Swap Usage: {swap_info.percent}% ({swap_info.free // (1024 * 1024)} MB Free)")
    if memory_info.percent > 85:
        publish_log("warning", f"🚨 High Memory Usage: {memory_info.percent}% used!")
    if swap_info.percent > 50:
        publish_log("warning", f"⚠️ High Swap Usage: {swap_info.percent}% used!")

def check_disk_status():
    """Monitor disk usage and detect critical storage issues."""
    disk_usage = psutil.disk_usage('/')
    publish_log("info", f"🗄 Disk Usage: {disk_usage.percent}% ({disk_usage.free // (1024 * 1024 * 1024)} GB Free)")
    if disk_usage.percent > 90:
        publish_log("warning", f"🚨 Low Disk Space: {disk_usage.percent}% used!")

def log_system_metrics():
    """Logs system metrics (CPU, RAM, Network, Disk) and checks for anomalies."""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    net_io = psutil.net_io_counters()
    net_sent = net_io.bytes_sent
    net_recv = net_io.bytes_recv
    disk_usage = psutil.disk_usage("/").percent
    disk_free = psutil.disk_usage("/").free // (1024 * 1024 * 1024)  # Convert to GB
    hostname = os.uname().nodename
    uptime = get_system_uptime()
    load_avg = get_load_average()

    metrics = {
        "cpu": cpu_usage,
        "ram": ram_usage,
        "net_sent": net_sent,
        "net_recv": net_recv,
        "disk_usage": disk_usage,
        "disk_free": disk_free,
        "hostname": hostname,
        "uptime": uptime,
        "load_avg": load_avg,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    redis_client.set("logninja_system_metrics", json.dumps(metrics))  # ✅ Store latest metrics
    redis_client.publish("logninja_system_stream", json.dumps(metrics))  # ✅ Publish live updates

def handle_anomalies(cpu_usage, ram_usage, network_spike):
    """Handle system anomalies and take necessary action."""
    if cpu_usage > 90 or ram_usage > 90:
        publish_log("critical", f"🚨 Critical Resource Usage! CPU: {cpu_usage}%, RAM: {ram_usage}%")
        os.system("sudo systemctl restart logninja")
    if network_spike:
        publish_log("warning", "🚨 Potential DDoS Detected! Taking action...")
        os.system("sudo iptables -A INPUT -s <Suspicious IP> -j DROP")  # Replace <Suspicious IP>

def run_system_monitor():
    """Run the core system monitoring process in a loop."""
    publish_log("info", "🚀 System Monitor Started!")
    while True:
        log_system_metrics()
        check_cpu_status()
        check_memory_status()
        check_disk_status()
        run_docker_monitor()  # ✅ Logs running Docker containers
        run_api_monitor()  # ✅ Logs API activity
        time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    run_system_monitor()
