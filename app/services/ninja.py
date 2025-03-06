import os
import time
import threading
import logging
from pathlib import Path
from app.services.ninja_actions import get_ninja_action
from colorama import Fore, Style, init

# 🛠 Initialize colorama for colored console output
init(autoreset=True)

# ✅ Ensure Logging is Configured Once
LOG_FILE = "/home/bruce/Projects/LogNinja-Core/logs/system_monitor.log"
LOG_DIR = os.path.dirname(LOG_FILE)

# Create log directory and file if they do not exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'w').close()

logger = logging.getLogger("LogNinja")
if not logger.hasHandlers():  # ✅ Prevent duplicate logging setups
    file_handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

# ✅ Global thread and lock to prevent duplicate cleanup processes
log_cleanup_thread = None
log_cleanup_lock = threading.Lock()

class NinjaLogManager:
    """🥷 Handles log cleanup and ninja-themed actions."""

    def __init__(self):
        self.logs_dir = Path(__file__).resolve().parent.parent / "logs"
        self.file_size_limit = 100 * 1024 * 1024  # 100MB
        self.ninja_action_interval = 180  # Every 3 minutes

    def delete_large_logs(self):
        """⚔️ Deletes logs ≥ 100MB to free space."""
        logger.info("🛠 Checking log file sizes...")
        deleted_files = []

        if self.logs_dir.exists():
            for log_file in self.logs_dir.glob("*.log"):
                if log_file.stat().st_size >= self.file_size_limit:
                    log_file.unlink()
                    deleted_files.append(log_file.name)

        if deleted_files:
            logger.info(f"🔥 Deleted {len(deleted_files)} large logs: {', '.join(deleted_files)}")
        return deleted_files

    def ninja_takes_break(self):
        """🎭 Logs AI-generated ninja actions dynamically every few minutes."""
        actions = get_ninja_action()
        for action in actions:
            logger.info(f"{Fore.CYAN}{action}{Style.RESET_ALL}")

    def log_cleanup_loop(self):
        """📜 Runs log cleanup and ninja messages in the background."""
        logger.info("🚀 Log Cleanup & Ninja Actions Started!")

        while True:
            self.delete_large_logs()
            self.ninja_takes_break()
            time.sleep(self.ninja_action_interval)  # Wait 3 minutes before logging ninja actions

# ✅ Define `log_manager`
log_manager = NinjaLogManager()

def start_ninja_log_cleanup():
    """🚀 Starts log cleanup & ninja actions in a separate thread."""
    global log_cleanup_thread
    with log_cleanup_lock:
        if log_cleanup_thread is None or not log_cleanup_thread.is_alive():
            log_cleanup_thread = threading.Thread(target=log_manager.log_cleanup_loop, daemon=True)
            log_cleanup_thread.start()
            logger.info("🚀 Log Cleanup Running in the Background!")
        else:
            logger.info("⚠️ Log cleanup is already running. No duplicate threads started.")