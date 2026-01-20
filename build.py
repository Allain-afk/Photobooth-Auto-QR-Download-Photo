"""
Build script for creating the Photobooth EXE
Works on all platforms and terminals
"""

import subprocess
import sys
import os
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

# Change to the script directory
os.chdir(SCRIPT_DIR)

print("=" * 60)
print("Building Photobooth EXE")
print("=" * 60)
print(f"\nWorking directory: {SCRIPT_DIR}")
print()

# Check if PyInstaller is installed
try:
    import PyInstaller
    print(f"✓ PyInstaller found: {PyInstaller.__version__}")
except ImportError:
    print("✗ PyInstaller not found!")
    print("\nInstalling PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✓ PyInstaller installed")

print("\n" + "=" * 60)
print("Building executable...")
print("=" * 60)
print()

# Build command
cmd = [
    sys.executable,
    "-m", "PyInstaller",
    "--name=Photobooth-QR",
    "--onefile",
    "--windowed",
    "--noconfirm",  # Don't ask for confirmation to overwrite
    "--clean",      # Clean cache before building
    "--hidden-import=watchdog",
    "--hidden-import=watchdog.observers",
    "--hidden-import=watchdog.observers.winapi",
    "--hidden-import=watchdog.events",
    "--hidden-import=PIL",
    "--hidden-import=PIL.Image",
    "--hidden-import=PIL.ImageTk",
    "--hidden-import=qrcode",
    "--hidden-import=config_manager",
    "--hidden-import=settings_gui",
    "--collect-all=watchdog",
    "photobooth.py"
]

print(f"Command: {' '.join(cmd)}\n")

# Run PyInstaller
try:
    result = subprocess.run(cmd, cwd=SCRIPT_DIR)
    
    if result.returncode == 0:
        exe_path = SCRIPT_DIR / "dist" / "Photobooth-QR.exe"
        
        print("\n" + "=" * 60)
        print("Build Complete!")
        print("=" * 60)
        print(f"\n✓ Executable created: {exe_path}")
        print(f"✓ Size: {exe_path.stat().st_size / (1024*1024):.1f} MB" if exe_path.exists() else "")
        print(f"\nLocation: dist\\Photobooth-QR.exe")
        print("\nYou can now:")
        print("  1. Run dist\\Photobooth-QR.exe to test")
        print("  2. Copy it to any Windows computer")
        print("  3. On first run, it will show settings window")
    else:
        print("\n✗ Build failed!")
        print(f"Exit code: {result.returncode}")
        sys.exit(1)
        
except Exception as e:
    print(f"\n✗ Error during build: {e}")
    sys.exit(1)
