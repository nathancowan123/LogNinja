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
    """Publishes logs to Redis for real-time monitoring."""
    log_entry = {"level": level, "message": message}
    redis_client.rpush("logninja_logs", json.dumps(log_entry))  # Store in Redis list
    redis_client.publish("logninja_stream", json.dumps(log_entry))  # Publish to Pub/Sub

def get_cpu_temp():
    """Retrieve CPU temperature (Linux/macOS)."""
    try:
        temps = psutil.sensors_temperatures().get("coretemp", [])
        return temps[0].current if temps else -1
    except Exception:
        return -1

def log_heavy_processes():
    """Logs the top 5 processes consuming the most CPU and memory."""
    publish_log("warning", "🔍 Analyzing high resource-consuming processes...")

    top_cpu = sorted(psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)[:5]
    for proc in top_cpu:
        publish_log("warning", f"⚡ High CPU Process: {proc.info['name']} (PID: {proc.info['pid']}) - {proc.info['cpu_percent']}% CPU")

    top_memory = sorted(psutil.process_iter(attrs=['pid', 'name', 'memory_percent']), key=lambda p: p.info['memory_percent'], reverse=True)[:5]
    for proc in top_memory:
        publish_log("warning", f"💾 High Memory Process: {proc.info['name']} (PID: {proc.info['pid']}) - {proc.info['memory_percent']:.2f}% Memory")

def kill_high_cpu_process():
    """Kill the highest CPU-consuming process."""
    high_cpu_processes = sorted(psutil.process_iter(attrs=['pid', 'cpu_percent']),
                                key=lambda p: p.info['cpu_percent'], reverse=True)
    if high_cpu_processes:
        highest_pid = high_cpu_processes[0].info['pid']
        os.system(f"kill -9 {highest_pid}")
        publish_log("critical", f"🛑 Killed high CPU process (PID: {highest_pid}) to prevent shutdown.")

def check_cpu_status():
    """Monitor CPU usage and temperature, triggering reboot if necessary."""
    global rebooting
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_temp = get_cpu_temp()

    publish_log("info", f"🖥 CPU Usage: {cpu_usage}%")
    publish_log("info", f"🌡 CPU Temp: {cpu_temp}°C")

    if cpu_usage > 80:
        publish_log("warning", f"🔥 High CPU Usage Detected: {cpu_usage}%")

    if cpu_temp >= CRITICAL_TEMP:
        publish_log("warning", f"⚠️ Warning: CPU Temperature High at {cpu_temp}°C!")

    if cpu_temp >= EMERGENCY_TEMP and not rebooting:
        rebooting = True
        publish_log("critical", f"💀 EMERGENCY TEMP {cpu_temp}°C REACHED! Rebooting immediately!")
        os.system("reboot now")
        return

    if cpu_temp >= CRITICAL_TEMP > 0 and not rebooting:
        publish_log("critical", f"💀 CRITICAL TEMP {cpu_temp}°C REACHED! Investigating before restart...")
        
        log_heavy_processes()
        run_docker_monitor()
        run_api_monitor()

        delay_time = 5 if cpu_temp >= 100 else 10 if cpu_temp >= 95 else 15 if cpu_temp >= 90 else SHUTDOWN_DELAY
        publish_log("critical", f"⏳ Delaying restart for {delay_time} seconds to allow intervention...")
        time.sleep(delay_time)

        if not rebooting:  # Double-check temp before rebooting
            publish_log("critical", "🔄 CRITICAL TEMP STILL HIGH! Attempting to kill high CPU process before restart.")
            kill_high_cpu_process()
            time.sleep(5)

            cpu_temp = get_cpu_temp()
            if cpu_temp >= CRITICAL_TEMP:
                publish_log("critical", "🔄 CRITICAL TEMP STILL HIGH! Initiating emergency restart.")
                rebooting = True
                os.system("reboot now")

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

def handle_anomalies(cpu_usage, ram_usage, network_spike):
    """Handle system anomalies and take necessary action."""
    if cpu_usage > 90 or ram_usage > 90:
        publish_log("critical", f"🚨 Critical Resource Usage! CPU: {cpu_usage}%, RAM: {ram_usage}%")
        os.system("sudo systemctl restart logninja")

    if network_spike:
        publish_log("warning", f"🚨 Potential DDoS Detected! Taking action...")
        os.system("sudo iptables -A INPUT -s <Suspicious IP> -j DROP")  # Replace <Suspicious IP>

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
