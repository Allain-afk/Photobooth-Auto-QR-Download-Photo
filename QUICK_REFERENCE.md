# Quick Reference Guide

## Building the EXE

```bash
# Method 1: Use the batch file
build_exe.bat

# Method 2: Direct command
pyinstaller --onefile --windowed --name="Photobooth-QR" photobooth.py
```

Output: `dist\Photobooth-QR.exe`

## Running the App

### First Time
1. Run `Photobooth-QR.exe`
2. Settings window appears
3. Set watch folder (where photos are saved)
4. Set Google Drive Folder ID
5. Click "Save & Start"

### After Configuration
- Just run `Photobooth-QR.exe`
- It starts monitoring automatically
- Settings saved in `photobooth_config.json`

## Reconfiguring

Delete `photobooth_config.json` and restart the app.

## Folder Structure

```
YourFolder/
├── Photobooth-QR.exe          # Main application
└── photobooth_config.json      # Auto-generated settings
```

## Settings File Format

```json
{
    "watch_folder": "C:\\Photos\\Output",
    "drive_folder_id": "1ABC123xyz",
    "qr_display_time": 30
}
```

## Keyboard Shortcuts

- `Escape` - Close popup
- `Click anywhere` - Close popup

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Popup not appearing | Check watch folder path is correct |
| QR code not working | Verify Google Drive folder is shared publicly |
| Settings not saving | Check write permissions in exe folder |
| Multiple popups | Each new photo gets its own popup (normal) |

## Google Drive Setup Checklist

- [ ] Google Drive for Desktop installed
- [ ] Created a folder for photos
- [ ] Folder is syncing to local computer
- [ ] Folder is shared: "Anyone with link can view"
- [ ] Copied folder ID from URL
- [ ] Entered ID in settings

## Support

For issues or questions, check:
- [README.md](README.md) - Full documentation
- [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) - Build details
