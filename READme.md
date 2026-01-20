# 📸 Photobooth QR Automation System

A local photobooth automation system that monitors a folder for new photos and displays a popup with a QR code linking to Google Drive for easy download.

## Features

- **Real-time Monitoring**: Watches a folder for new `.jpg` and `.png` files using the `watchdog` library
- **QR Code Generation**: Instantly generates a QR code pointing to your Google Drive
- **Beautiful UI**: Modern, borderless popup window with photo preview and QR code
- **Auto-close**: Popup automatically closes after 30 seconds (configurable)
- **Multi-threading**: Can handle multiple photos in quick succession

## Installation

1. **Install Python 3.8+** if not already installed

2. **Install dependencies**:
   ```bash
   cd "C:\Users\user\Documents\Photobooth"
   pip install -r requirements.txt
   ```

## Configuration

Open `photobooth_qr.py` and modify the configuration section at the top:

```python
# Folder to monitor for new photos
WATCH_FOLDER = r"C:\Photobooth\Outputs"

# Time in seconds before the popup automatically closes
QR_DISPLAY_TIME = 30

# Your Google Drive shared folder ID
DRIVE_FOLDER_ID = "YOUR_GOOGLE_DRIVE_FOLDER_ID_HERE"
```

### Getting Your Google Drive Folder ID

1. Open Google Drive in your browser
2. Navigate to the folder you want to share
3. Click **Share** and set it to "Anyone with the link can view"
4. Copy the folder URL (e.g., `https://drive.google.com/drive/folders/1ABC123xyz`)
5. The folder ID is the part after `/folders/` → `1ABC123xyz`

### Setting Up Google Drive for Desktop

1. Install [Google Drive for Desktop](https://www.google.com/drive/download/)
2. Configure it to sync your `WATCH_FOLDER` to Google Drive
3. Share the synced folder publicly

## Usage

1. **Start the application**:
   ```bash
   python photobooth_qr.py
   ```

2. **Take photos** - When your photobooth software saves a new `.jpg` or `.png` to the watched folder, the popup will automatically appear

3. **Scan the QR code** - Guests can scan with their phone camera to access the Google Drive folder

## UI Preview

The popup window displays:
- 📷 **Left**: Photo preview (scaled to fit)
- 📱 **Right**: QR code for scanning
- ⏱️ **Bottom**: Countdown timer

Click anywhere or press `Escape` to close the popup early.

## Customization

### UI Colors

Modify these variables in the configuration section:

```python
BACKGROUND_COLOR = "#1a1a2e"   # Dark blue background
ACCENT_COLOR = "#0f3460"       # Frame accent
TEXT_COLOR = "#e8e8e8"         # Light text
HEADER_COLOR = "#00d4ff"       # Cyan header
```

### Window Size

```python
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 520
PHOTO_SIZE = (400, 400)
QR_SIZE = 300
```

### Custom Drive URL Logic

To implement direct file linking (requires Google Drive API), modify the `get_drive_url()` function:

```python
def get_drive_url(filename: str) -> str:
    # Implement your custom logic here
    # Example: Call Google Drive API to get file ID
    file_id = lookup_file_id(filename)  # Your implementation
    return f"https://drive.google.com/file/d/{file_id}/view"
```

## Troubleshooting

### Popup not appearing?
- Check that the `WATCH_FOLDER` path is correct
- Ensure the folder exists
- Verify the photo file has a `.jpg`, `.jpeg`, or `.png` extension

### QR code not working?
- Verify `DRIVE_FOLDER_ID` is correct
- Ensure the Google Drive folder is shared publicly
- Check that Google Drive for Desktop is syncing properly

### Multiple popups?
- This is by design! Each new photo gets its own popup
- Close popups by clicking anywhere or pressing `Escape`

## Tech Stack

- **Python 3.8+**
- **watchdog** - File system monitoring
- **Pillow (PIL)** - Image processing
- **qrcode** - QR code generation
- **Tkinter** - GUI framework (included with Python)

## License

MIT License - Feel free to modify and use for your photobooth events!

