import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

import colorlog

LOG_LEVEL = logging.INFO
LOG_FORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(name)-7s | %(log_color)s%(message)s%(reset)s"
LOG_FORMAT_FILE = "%(asctime)s | %(levelname)-8s | %(name)-7s | %(message)s"


def setup_logging(log_file: Optional[str] = None) -> None:
    """Configures the logging module with colored level and message formatting.
    
    Args:
        log_file: Optional path to a log file. If provided, logs will be written to both
                  console (with colors) and file (without colors, with timestamps).
                  Supports rotation to prevent huge files (max 10MB, 5 backups).
    """

    print(f"[DEBUG] setup_logging called with log_file={log_file}")

    logging.root.setLevel(LOG_LEVEL)
    
    # Console handler with colors
    formatter = colorlog.ColoredFormatter(LOG_FORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(LOG_LEVEL)
    root.addHandler(stream)
    
    print(f"[DEBUG] Console logging configured")
    
    # Optional file handler (without colors, with timestamps)
    if log_file:
        print(f"[DEBUG] Setting up file handler for: {log_file}")
        log_path = Path(log_file).expanduser().resolve()
        print(f"[DEBUG] Resolved log path: {log_path}")
        log_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"[DEBUG] Created parent directory: {log_path.parent}")
        
        file_formatter = logging.Formatter(LOG_FORMAT_FILE)
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(file_formatter)
        root.addHandler(file_handler)
        
        print(f"[DEBUG] File handler added to root logger")
        
        # Log that file logging is enabled
        logging.info(f"File logging enabled: {log_path}")
        print(f"[DEBUG] Logged info message about file logging")
    else:
        print(f"[DEBUG] No log file specified, console-only mode")
