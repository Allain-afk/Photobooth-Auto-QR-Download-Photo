# 📸 Photobooth QR - User Guide

## What is this?

This app automatically creates QR codes for your photobooth photos so guests can easily download them to their phones.

## How it works

1. **You take a photo** with your photobooth
2. **Photo gets saved** to the folder you configured
3. **Popup appears** automatically showing:
   - Preview of the photo
   - QR code for downloading
4. **Guest scans QR code** with their phone camera
5. **Opens Google Drive** where they can download the photo

## First Time Setup

### Step 1: Run the App

Double-click `Photobooth-QR.exe`

### Step 2: Configure Settings

A settings window will appear with 3 things to configure:

#### 📁 Watch Folder
- This is where your photobooth saves photos
- Example: `C:\Photobooth\Photos`
- Click "Browse..." to select it
- If the folder doesn't exist, the app will create it

#### ☁️ Google Drive Folder ID
- This is from your Google Drive folder URL
- Example URL: `https://drive.google.com/drive/folders/1ABC123xyz`
- The ID is: `1ABC123xyz`
- See "Setting Up Google Drive" below

#### ⏱️ Auto-close Time
- How long the popup stays open (in seconds)
- Default: 30 seconds
- Guest can close it early by clicking or pressing Escape

### Step 3: Save & Start

Click the green "Save & Start" button. The app will now run in the background!

## Setting Up Google Drive

This is a one-time setup:

### 1. Install Google Drive for Desktop

Download from: https://www.google.com/drive/download/

### 2. Create a Folder for Photos

1. Open Google Drive in your web browser
2. Create a new folder (e.g., "Photobooth Photos")
3. This folder will store all your event photos

### 3. Set Up Syncing

1. Open Google Drive for Desktop (system tray icon)
2. Set up the folder to sync with your computer
3. Make sure your photobooth saves photos to the synced folder

### 4. Share the Folder Publicly

**IMPORTANT:** The folder must be publicly shared for QR codes to work!

1. Right-click the folder in Google Drive
2. Click "Share"
3. Click "Change" next to "Restricted"
4. Select "Anyone with the link"
5. Make sure permission is set to "Viewer"
6. Click "Done"

### 5. Get the Folder ID

1. Open the folder in Google Drive (web browser)
2. Look at the URL in the address bar
3. It will look like: `https://drive.google.com/drive/folders/1ABC123xyz`
4. Copy everything after `/folders/` → That's your Folder ID!
5. Paste it into the app settings

## Daily Use

### Starting the App

Just double-click `Photobooth-QR.exe` - it will start monitoring automatically!

### When a Photo is Taken

1. Photobooth saves the photo
2. Popup appears within seconds
3. Guest can scan the QR code immediately

### Popup Features

- **Photo Preview** - Shows the photo that was just taken
- **QR Code** - Scan with any phone camera app
- **Auto-close** - Closes automatically after the set time
- **Manual close** - Click anywhere or press Escape

### Multiple Guests

If multiple photos are taken quickly, each gets its own popup window. They'll appear slightly offset so you can see all of them.

## Troubleshooting

### "Popup not appearing"

**Check:**
- Is the watch folder path correct?
- Does the photo have .jpg or .png extension?
- Is the app still running? (check Task Manager)

**Fix:**
- Reconfigure settings (delete `photobooth_config.json`)
- Make sure folder exists and has correct permissions

### "QR code doesn't work when scanned"

**Check:**
- Is the Google Drive folder shared publicly?
- Did you enter the correct Folder ID?
- Is your phone connected to the internet?

**Fix:**
1. Go to Google Drive (web browser)
2. Find your folder
3. Right-click → Share
4. Make sure it says "Anyone with the link"
5. Copy the folder ID again and reconfigure

### "Photos not uploading to Google Drive"

**Check:**
- Is Google Drive for Desktop running?
- Is the folder set to sync?
- Do you have internet connection?

**Fix:**
1. Check Google Drive system tray icon
2. Click it and check sync status
3. Make sure the folder is marked for syncing

### "Settings window won't open"

The settings window only appears on first run or if config is missing.

**To reconfigure:**
1. Close the app
2. Delete `photobooth_config.json` (in same folder as .exe)
3. Run the app again

## Tips & Best Practices

✅ **Test before your event**
- Take a test photo
- Scan the QR code yourself
- Make sure it opens Google Drive

✅ **Keep app running**
- Start it before the event
- It runs in the background
- Check Task Manager if you're not sure

✅ **Organize by event**
- Create a new folder for each event
- Update the Folder ID in settings
- Makes it easier for guests to find their photos

✅ **Internet connection**
- Both you and guests need internet
- For scanning QR codes and accessing Drive
- Consider WiFi availability at your venue

✅ **Backup settings**
- Keep a copy of `photobooth_config.json`
- Quick restore if something goes wrong

## File Locations

When you run the app, it creates:

```
📁 Your Folder
├── 📄 Photobooth-QR.exe        ← The application
└── 📄 photobooth_config.json   ← Your settings (auto-created)
```

## Need to Reconfigure?

1. **Stop the app** (close it or end in Task Manager)
2. **Delete** `photobooth_config.json`
3. **Run the app again** - settings window will appear

## Questions?

Check the other documentation files:
- `README.md` - Full technical documentation
- `QUICK_REFERENCE.md` - Quick command reference
- `BUILD_INSTRUCTIONS.md` - How to rebuild the .exe

---

**Enjoy your photobooth! 📸✨**
