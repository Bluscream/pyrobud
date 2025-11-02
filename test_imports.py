#!/usr/bin/env python3
import sys
import traceback

print("Testing imports...")

try:
    print("1. async_helpers...", end=" ")
    import pyrobud.util.async_helpers
    print("✓")
except Exception as e:
    print(f"✗ {e}")
    traceback.print_exc()

try:
    print("2. config...", end=" ")
    import pyrobud.util.config
    print("✓")
except Exception as e:
    print(f"✗ {e}")
    traceback.print_exc()

try:
    print("3. db...", end=" ")
    import pyrobud.util.db
    print("✓")
except Exception as e:
    print(f"✗ {e}")
    traceback.print_exc()

print("Done!")

