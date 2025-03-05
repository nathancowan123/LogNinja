import logging
import logging.config
import os

# Define log directory
LOG_DIR = "/home/bruce/Projects/LogNinja-Core/logs"
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure the logs folder exists

# Ensure log files exist before writing to them
log_files = ["errors.log", "ratelimits.log", "unauthorized.log", "logninja.log", "logninja_master.log"]

for log_file in log_files:
    log_path = os.path.join(LOG_DIR, log_file)
    if not os.path.exists(log_path):
        open(log_path, "w").close()  # Create an empty file if it doesn't exist

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "detailed": {
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    },

    "handlers": {
        "error_file_handler": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "errors.log"),
            "formatter": "detailed",
            "level": "ERROR"
        },
        "ratelimit_file_handler": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "ratelimits.log"),
            "formatter": "detailed",
            "level": "INFO"
        },
        "unauthorized_file_handler": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "unauthorized.log"),
            "formatter": "detailed",
            "level": "INFO"
        },
        "main_file_handler": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "logninja.log"),
            "formatter": "detailed",
            "level": "DEBUG"
        },
        "master_file_handler": {  # ✅ Capture EVERYTHING in master log
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "logninja_master.log"),
            "formatter": "detailed",
            "level": "DEBUG"
        }
    },

    "loggers": {
        "errors": {
            "level": "ERROR",
            "handlers": ["error_file_handler", "master_file_handler"],  # ✅ Also logs to master
            "propagate": False
        },
        "ratelimits": {
            "level": "INFO",
            "handlers": ["ratelimit_file_handler", "master_file_handler"],  # ✅ Also logs to master
            "propagate": False
        },
        "unauthorized": {
            "level": "INFO",
            "handlers": ["unauthorized_file_handler", "master_file_handler"],  # ✅ Also logs to master
            "propagate": False
        },
        "main": {
            "level": "DEBUG",
            "handlers": ["main_file_handler", "master_file_handler"],  # ✅ Also logs to master
            "propagate": True
        }
    },

    # ✅ Root Logger - Captures **EVERYTHING** not explicitly named
    "root": {
        "level": "DEBUG",
        "handlers": ["master_file_handler"]
    }
}


# Apply the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

# Create loggers
error_logger = logging.getLogger("errors")
ratelimit_logger = logging.getLogger("ratelimits")
unauthorized_logger = logging.getLogger("unauthorized")
main_logger = logging.getLogger("main")

# Test Log Entries
main_logger.info("🚀 LogNinja logging initialized!")
error_logger.error("🔥 This is a test ERROR log")
ratelimit_logger.info("⏳ Rate limit exceeded for IP: 192.168.1.100")
unauthorized_logger.info("🚫 Unauthorized access attempt detected")
main_logger.info("📡 All logs now also go to logninja_master.log!")
