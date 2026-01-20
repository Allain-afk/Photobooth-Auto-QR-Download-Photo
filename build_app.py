"""
Build script for creating standalone EXE
"""

import subprocess
import sys
from pathlib import Path

print("=" * 60)
print("Building Photobooth Pro EXE")
print("=" * 60)

# Build command
cmd = [
    sys.executable,
    "-m", "PyInstaller",
    "--name=PhotoboothPro",
    "--onefile",
    "--windowed",
    "--noconfirm",
    "--clean",
    "--add-data=core;core",
    "--add-data=ui;ui",
    "--add-data=utils;utils",
    "--hidden-import=PIL._tkinter_finder",
    "--hidden-import=cv2",
    "main.py"
]

print(f"\nRunning: {' '.join(cmd)}\n")

result = subprocess.run(cmd)

if result.returncode == 0:
    print("\n" + "=" * 60)
    print("Build Complete!")
    print("=" * 60)
    print(f"\nEXE location: dist\\PhotoboothPro.exe")
    print("\nYou can now distribute this file!")
else:
    print("\n✗ Build failed!")
    sys.exit(1)
