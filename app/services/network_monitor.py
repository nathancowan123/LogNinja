import psutil
import time
import logging
import threading

# ✅ Configure logging
logging.basicConfig(filename="/home/bruce/Projects/LogNinja-Core/logs/network.log", level=logging.WARNING)

class NetworkMonitor:
    def __init__(self):
        self.prev_sent = psutil.net_io_counters().bytes_sent
        self.prev_recv = psutil.net_io_counters().bytes_recv

    def check_network_spike(self):
        """Monitors network traffic for sudden spikes."""
        net_io = psutil.net_io_counters()

        sent_diff = net_io.bytes_sent - self.prev_sent
        recv_diff = net_io.bytes_recv - self.prev_recv

        self.prev_sent = net_io.bytes_sent
        self.prev_recv = net_io.bytes_recv

        if sent_diff > 10_000_000 or recv_diff > 10_000_000:  # ✅ Detects 10MB+ network spikes
            logging.warning(f"🚨 Network Spike! Sent: {sent_diff} bytes, Received: {recv_diff} bytes")

    def run_monitor(self):
        """Runs network monitoring in a loop."""
        while True:
            self.check_network_spike()
            time.sleep(10)  # ✅ Adjust interval as needed

# ✅ Ensure `api_monitor.py` is only imported **inside** the function
def start_network_monitor():
    from app.services.api_monitor import start_api_monitor  # ✅ Moved import inside function

    network_monitor = NetworkMonitor()
    monitor_thread = threading.Thread(target=network_monitor.run_monitor, daemon=True, name="NetworkMonitorThread")
    monitor_thread.start()
    
    start_api_monitor()  # ✅ Start API monitor after network monitor starts
