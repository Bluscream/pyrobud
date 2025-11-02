#!/usr/bin/env python3
"""Test if debug code is in the installed version."""

import sys
print("1. Importing pyrobud...")
import pyrobud
print(f"   Location: {pyrobud.__file__}")

print("2. Importing main module...")
from pyrobud import main
print("   Success!")

print("3. Checking for debug code...")
import inspect
try:
    source = inspect.getsource(main)
    has_debug = '[DEBUG]' in source
    print(f"   Has debug statements: {has_debug}")
    if has_debug:
        print("   ✓ Debug code is present!")
    else:
        print("   ✗ Debug code NOT found - need to reinstall")
except Exception as e:
    print(f"   Error: {e}")

print("4. Checking main.py file directly...")
import pathlib
main_file = pathlib.Path(pyrobud.__file__).parent / "main.py"
if main_file.exists():
    content = main_file.read_text()
    has_debug_file = '[DEBUG]' in content
    print(f"   File has debug: {has_debug_file}")
    if has_debug_file:
        print(f"   First few lines with DEBUG:")
        for i, line in enumerate(content.splitlines()):
            if '[DEBUG]' in line:
                print(f"   Line {i+1}: {line[:80]}")
else:
    print(f"   main.py not found at {main_file}")

