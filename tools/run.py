#!/usr/bin/env python3
"""
Standalone launcher for pyrobud - runs without pip install.
Adds the project root to Python path so pyrobud package can be imported.
"""

import sys
from pathlib import Path

# Add project root directory to Python path
# This script is in tools/, so go up one level to get project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now import and run pyrobud
from pyrobud.main import main

if __name__ == "__main__":
    main()
