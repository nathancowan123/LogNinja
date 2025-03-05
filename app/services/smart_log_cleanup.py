import os
import shutil
import gzip
import time
from datetime import datetime, timedelta

LOG_DIR = "/home/bruce/Projects/LogNinja-Core/logs"
ARCHIVE_DIR = "/home/bruce/Projects/LogNinja-Core/logs_archive"
RETENTION_DAYS = 7  # Keep logs from the last 7 days
DISK_THRESHOLD = 0.90  # Delete only if disk is over 90% full

os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive folder exists

def compress_log(file_path):
    """Compress logs before archiving."""
    with open(file_path, "rb") as f_in:
        with gzip.open(file_path + ".gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(file_path)  # Remove original file after compression

def cleanup_old_logs():
    """Move old logs to archive, delete only if disk space is critical."""
    total, used, free = shutil.disk_usage("/")
    
    now = datetime.now()
    for file in os.listdir(LOG_DIR):
        file_path = os.path.join(LOG_DIR, file)

        if os.path.isfile(file_path) and not file.endswith(".gz"):  # Skip already compressed logs
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            file_age = now - file_time
            
            if file_age > timedelta(days=RETENTION_DAYS):  
                archive_path = os.path.join(ARCHIVE_DIR, file + ".gz")
                compress_log(file_path)
                shutil.move(file_path + ".gz", archive_path)
                print(f"📦 Archived: {file} → {archive_path}")

    # If disk usage is critical (90%+), delete oldest logs from archive
    if used / total > DISK_THRESHOLD:
        archive_files = sorted(os.listdir(ARCHIVE_DIR), key=lambda f: os.path.getmtime(os.path.join(ARCHIVE_DIR, f)))
        if archive_files:
            oldest_file = os.path.join(ARCHIVE_DIR, archive_files[0])
            os.remove(oldest_file)
            print(f"🚨 Disk Full! Deleted Oldest Archived Log: {oldest_file}")

cleanup_old_logs()

# 🚀 How It Works

# 🔹 Logs Stay for 7 Days in /logs/
# 🔹 Older Logs Are Moved & Compressed in /logs_archive/
# 🔹 Nothing is Deleted Until Disk is 90% Full
# 🔹 If Disk Fills, Only Oldest Archive is Removed

# ✅ Your forensic logs remain intact, but space is managed properly! Let me know if you want tweaks! 