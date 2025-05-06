import logging
import os
from logging.handlers import TimedRotatingFileHandler

base_log_dir = "logs"
error_log_dir = os.path.join(base_log_dir, "errors")
info_log_dir = os.path.join(base_log_dir, "info")
backup_count = 15
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

os.makedirs(error_log_dir, exist_ok=True)
os.makedirs(info_log_dir, exist_ok=True)

# --- Error log handler (only errors) ---
error_handler = TimedRotatingFileHandler(
    filename=os.path.join(error_log_dir, "errors.log"),
    when="midnight",
    interval=1,
    backupCount=backup_count,
    encoding="utf-8",
)
error_handler.setLevel(logging.ERROR)  # Only log ERROR and CRITICAL
error_handler.setFormatter(formatter)

# --- General log handler (everything) ---
general_handler = TimedRotatingFileHandler(
    filename=os.path.join(info_log_dir, "info.log"),
    when="midnight",
    interval=1,
    backupCount=backup_count,
    encoding="utf-8",
)
general_handler.setLevel(logging.DEBUG)  # Log everything (DEBUG and above)
general_handler.setFormatter(formatter)

# --- Logger setup ---
logger = logging.getLogger("scraper")
logger.setLevel(logging.DEBUG)  # Capture all log levels
logger.addHandler(error_handler)  # Add error handler
logger.addHandler(general_handler)  # Add general handler
logger.propagate = False  # Avoid duplicates

# --- Flag-specific logger (e.g., logs/flagged/flagged.log) ---
flagged_log_dir = os.path.join(base_log_dir, "flagged")
os.makedirs(flagged_log_dir, exist_ok=True)

flagged_handler = TimedRotatingFileHandler(
    filename=os.path.join(flagged_log_dir, "flagged.log"),
    when="midnight",
    interval=1,
    backupCount=backup_count,
    encoding="utf-8",
)
flagged_handler.setLevel(logging.INFO)
flagged_handler.setFormatter(formatter)

# Create a dedicated logger
flagged_logger = logging.getLogger("scraper.flagged")
flagged_logger.setLevel(logging.INFO)
flagged_logger.addHandler(flagged_handler)
flagged_logger.propagate = False  # Prevent duplication
