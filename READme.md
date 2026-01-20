# Photobooth Pro - Professional Photobooth Software

A free, open-source alternative to commercial photobooth software like DSLRBooth.

## Features

- 🖥️ **Standalone EXE** - No Python installation required for end users
- ⚙️ **Easy Configuration** - GUI settings window on first run
- 📁 **Auto-monitoring** - Watches any folder for new photos
- ☁️ **Google Drive Integration** - QR codes link to your shared folder
- ⏱️ **Auto-close popups** - Configurable timeout

## Quick Start (Using EXE)

### For End Users

1. **Download** the `Photobooth-QR.exe` file
2. **Double-click** to run
3. **Configure settings** in the popup window:
   - Set the folder where photos are saved
   - Enter your Google Drive Folder ID
   - Set auto-close time (default: 30 seconds)
4. **Click "Save & Start"**

The app will now monitor your folder and show popups with QR codes!

### Getting Google Drive Folder ID

1. Install [Google Drive for Desktop](https://www.google.com/drive/download/)
2. Create a folder in Google Drive for your photos
3. Set up sync for your photobooth output folder
4. Share the folder: Right-click → Share → "Anyone with link can view"
5. Copy the folder URL: `https://drive.google.com/drive/folders/YOUR_FOLDER_ID`
6. The ID is the part after `/folders/` → Use this in settings

## Development Setup

### For Developers

If you want to modify the code or build the EXE yourself:

1. **Install Python 3.8+**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run from source**:
   ```bash
   python photobooth.py
   ```

4. **Build EXE**:
   ```bash
   # Windows
   build_exe.bat
   
   # Or manually
   pyinstaller --onefile --windowed --name="Photobooth-QR" photobooth.py
   ```

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for detailed build steps.

## Configuration

Settings are saved in `photobooth_config.json` which is created automatically.

To reconfigure after first run:
- Delete `photobooth_config.json` and restart
- Or edit the JSON file directly

## Files

- `photobooth.py` - Main application
- `config_manager.py` - Configuration handler
- `settings_gui.py` - Settings window
- `build_exe.bat` - Windows build script
- `photobooth.spec` - PyInstaller configuration

## Requirements

- Python 3.8+ (for development only)
- Windows OS (for EXE)
- Google Drive for Desktop (for photo sync)


