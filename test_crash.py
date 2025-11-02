#!/usr/bin/env python3
import sys

print("Step 1: Import pyrobud package")
sys.stdout.flush()
import pyrobud
print("OK pyrobud")
sys.stdout.flush()

print("Step 2: Import version")
sys.stdout.flush()
from pyrobud import version
print("OK version")
sys.stdout.flush()

print("Step 3: Import logs")
sys.stdout.flush()
from pyrobud import logs
print("OK logs")
sys.stdout.flush()

print("Step 4: Import util modules individually")
sys.stdout.flush()

modules_to_test = [
    "async_helpers",
    "config",
    "db",
    "error",
    "git",
    "image",
    "misc",
    "sentry",
    "system",
    "text",
    "tg",
    "time",
    "version",
]

for mod in modules_to_test:
    print(f"  4.{mod}...", end=" ")
    sys.stdout.flush()
    try:
        exec(f"from pyrobud.util import {mod}")
        print("OK")
        sys.stdout.flush()
    except Exception as e:
        print(f"FAIL {e}")
        sys.stdout.flush()
        import traceback
        traceback.print_exc()
        break

print("All imports successful!")
