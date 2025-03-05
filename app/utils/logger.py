import logging
import os

# ✅ Configure logging
LOG_FILE = "logs/system_monitor.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("LogNinja")

def log_message(message, level="info"):
    """Logs messages at different levels (INFO, WARNING, CRITICAL)."""
    getattr(logger, level)(message)
    print(message)
