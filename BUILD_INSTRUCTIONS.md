# How to Build the Photobooth EXE

This guide explains how to create a standalone `.exe` file for Windows.

## Prerequisites

1. Python 3.8+ installed
2. All dependencies installed: `pip install -r requirements.txt`

## Build Steps

### Option 1: Using the Build Script (Easiest)

```bash
# Just run the batch file
build_exe.bat
```

The exe will be created in the `dist` folder.

### Option 2: Using PyInstaller Directly

```bash
# Simple one-file build
pyinstaller --onefile --windowed --name="Photobooth-QR" photobooth.py
```

### Option 3: Using the Spec File (Advanced)

```bash
# Use the custom spec file for more control
pyinstaller photobooth.spec
```

## After Building

1. The executable will be in: `dist\Photobooth-QR.exe`
2. Copy `Photobooth-QR.exe` to any folder
3. Double-click to run
4. On first run, settings window will appear
5. Configure your folders and Google Drive ID
6. Settings are saved in `photobooth_config.json` next to the exe

## Distribution

You can copy the `Photobooth-QR.exe` to any Windows computer. No Python installation required on the target machine!

## Troubleshooting

### "Missing module" errors
- Make sure all dependencies are installed before building
- Try rebuilding with `--hidden-import=module_name`

### Antivirus blocking
- Some antivirus programs flag PyInstaller executables
- You may need to add an exception

### Console window appears
- Make sure you used `--windowed` flag
- Or edit `photobooth.spec` and set `console=False`

## Build Options Explained

- `--onefile`: Creates a single exe file (vs. folder with dependencies)
- `--windowed`: No console window (GUI only)
- `--name="Photobooth-QR"`: Name of the output exe
- `--icon=icon.ico`: Add a custom icon (if you have one)

## File Size

The exe will be approximately 20-30 MB because it includes:
- Python runtime
- All required libraries (Pillow, watchdog, qrcode, tkinter)
- Your application code

This is normal for PyInstaller builds!
