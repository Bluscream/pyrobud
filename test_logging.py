#!/usr/bin/env python3
"""Quick test script for file logging functionality."""

import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

print("1. Importing pyrobud modules...")
from pyrobud import logs

print("2. Setting up logging with file: pyrobud_test.log")
logs.setup_logging(log_file='pyrobud_test.log')

print("3. Creating test logger...")
log = logging.getLogger('test')

print("4. Writing test messages...")
log.info("Test message 1: File logging works!")
log.warning("Test message 2: This is a warning")
log.error("Test message 3: This is an error")

print("5. Checking if log file was created...")
log_path = Path('pyrobud_test.log')
if log_path.exists():
    print(f"✅ SUCCESS! Log file created at: {log_path.resolve()}")
    print(f"   Size: {log_path.stat().st_size} bytes")
    print("\n--- Log file content ---")
    print(log_path.read_text())
else:
    print("❌ FAILED: Log file not created")

print("\nTest complete!")
