#!/usr/bin/env python3
"""
Standalone launcher for pyrobud - runs without pip install.
Adds the current directory to Python path so pyrobud package can be imported.
"""

import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Now import and run pyrobud
from pyrobud.main import main

if __name__ == "__main__":
    main()
