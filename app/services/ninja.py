import os
import time
import threading
import logging
import shutil
import psutil  # To check RAM usage
from pathlib import Path
from app.services.ninja_actions import get_ninja_action
from colorama import Fore, Style, init

# Initialize colorama for colors
init(autoreset=True)

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
FILE_SIZE_LIMIT = 100 * 1024 * 1024  # 100MB
INACTIVITY_THRESHOLD = 180  # 3 minutes
RAM_THRESHOLD_PERCENT = 80  # Clear cache if RAM usage exceeds 80%
FREE_RAM_THRESHOLD_MB = 1024  # Clear if free RAM drops below 1GB

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("LogNinja")

class NinjaLogManager:
    """🥷 Manages log cleaning, cache clearing, and system optimization."""
    
    def __init__(self):
        self.last_action_time = time.time()

    def delete_large_logs(self):
        """⚔️ Deletes logs ≥ 100MB."""
        deleted_files = []
        if LOGS_DIR.exists():
            for filename in os.listdir(LOGS_DIR):
                file_path = LOGS_DIR / filename
                if file_path.suffix == ".log" and file_path.is_file():
                    file_size = file_path.stat().st_size
                    if file_size >= FILE_SIZE_LIMIT:
                        file_path.unlink()
                        deleted_files.append({"file": filename, "size_mb": round(file_size / (1024 * 1024), 2)})
        
        if deleted_files:
            logger.info(f"{Fore.RED}🥷⚡ {len(deleted_files)} bloated logs SLASHED! ⚔️🔥{Style.RESET_ALL}")
            for f in deleted_files:
                logger.info(f"{Fore.YELLOW}📜 {f['file']} | 💾 {f['size_mb']} MB [Erased!]{Style.RESET_ALL}")
        
        return deleted_files

    def check_and_clear_ram_cache(self):
        """🧹 Checks RAM usage and clears cache if necessary."""
        ram = psutil.virtual_memory()
        used_percent = ram.percent
        free_mb = ram.available / (1024 * 1024)  # Convert bytes to MB

        if used_percent > RAM_THRESHOLD_PERCENT or free_mb < FREE_RAM_THRESHOLD_MB:
            logger.info(f"{Fore.RED}💾 RAM usage high ({used_percent}%) or free RAM low ({free_mb:.2f}MB). Clearing cache...{Style.RESET_ALL}")
            self.clear_ram_cache()
        else:
            logger.info(f"{Fore.GREEN}💾 RAM usage at {used_percent}% ({free_mb:.2f}MB free). No action needed.{Style.RESET_ALL}")

    def clear_ram_cache(self):
        """⚡ Clears RAM cache based on the OS."""
        try:
            if os.name == "posix":  # Linux & macOS
                os.system("sync; echo 3 > /proc/sys/vm/drop_caches")
                logger.info(f"{Fore.CYAN}🧹 Log Ninja purged the system cache! ⚔️💨{Style.RESET_ALL}")
            elif os.name == "nt":  # Windows
                import ctypes
                ctypes.windll.psapi.EmptyWorkingSet(-1)
                logger.info(f"{Fore.CYAN}🧹 Log Ninja cleared Windows standby memory! ⚔️💨{Style.RESET_ALL}")
            else:
                logger.warning(f"{Fore.YELLOW}⚠️ Cache clearing is not supported on this OS.{Style.RESET_ALL}")
        except Exception as e:
            logger.error(f"{Fore.RED}❌ Failed to clear cache: {e}{Style.RESET_ALL}")

    def monitor_logs(self):
        """📜 Monitors logs, RAM, and updates ninja status."""
        while True:
            deleted_files = self.delete_large_logs()
            self.check_and_clear_ram_cache()
            current_time = time.time()

            if not deleted_files:
                time_since_last_action = current_time - self.last_action_time
                if time_since_last_action > INACTIVITY_THRESHOLD:
                    self.ninja_takes_break()
                else:
                    logger.info(f"{Fore.GREEN}🕵️‍♂️ No logs detected... Ninja rests. 💤{Style.RESET_ALL}")

            time.sleep(30)  # ✅ Runs every 30 seconds

    def ninja_takes_break(self):
        """⏳ Uses AI to generate ninja actions dynamically."""
        actions = get_ninja_action()
        for action in actions:
            logger.info(f"{Fore.CYAN}{action}{Style.RESET_ALL}")

log_manager = NinjaLogManager()
