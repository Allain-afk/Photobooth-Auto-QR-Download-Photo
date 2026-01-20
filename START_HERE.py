"""
Quick Start Guide for Photobooth Pro
"""

print("""
╔══════════════════════════════════════════════════════════════╗
║         PHOTOBOOTH PRO - QUICK START GUIDE                   ║
╚══════════════════════════════════════════════════════════════╝

🎉 Welcome to Photobooth Pro!

Your new professional photobooth software is ready to use!

📋 WHAT WAS CREATED:

✅ Full photobooth application with:
   • Camera support (Webcam & DSLR)
   • Touch-friendly fullscreen interface
   • Countdown timer
   • Photo review screen
   • Settings panel
   • Auto-save photos
   • Print & email support (configurable)

📁 PROJECT STRUCTURE:

   main.py              ← Start the application
   core/                ← Core functionality
   ├── camera_manager.py
   └── settings_manager.py
   ui/                  ← User interface
   ├── main_window.py
   ├── screens.py
   └── settings_panel.py
   utils/               ← Utilities
   └── logger.py

🚀 HOW TO RUN:

   1. Run the app:
      python main.py

   2. On first run, it will:
      • Create settings file
      • Initialize webcam
      • Show fullscreen interface

   3. Controls:
      • TAP SCREEN or click START button
      • Ctrl+S = Settings panel
      • Escape/F11 = Toggle fullscreen
      
⚙️ CONFIGURATION:

   Press Ctrl+S while running to access settings:
   • Camera type (Webcam/DSLR)
   • Resolution
   • Event name
   • Save folder
   • Countdown time
   • Photo overlays
   • Print & email options

📸 FEATURES:

   ✓ Webcam support (works out of the box)
   ✓ DSLR support (requires gphoto2)
   ✓ Live preview
   ✓ Countdown timer
   ✓ Photo review
   ✓ Auto-save
   ✓ Customizable overlays/templates
   ✓ Print integration
   ✓ Email sharing

🎨 PHOTO OVERLAYS:

   1. Create PNG with transparency
   2. Size: Match your camera resolution
   3. Enable in Settings → Advanced
   4. Browse to your overlay file

🏗️ BUILD EXE:

   python build_app.py
   
   Creates: dist/PhotoboothPro.exe

📖 MORE INFO:

   See README.md for detailed documentation

═══════════════════════════════════════════════════════════════

🎊 READY TO GO!

Run:  python main.py

This is a COMPLETE photobooth app similar to DSLRBooth!

═══════════════════════════════════════════════════════════════
""")

print("\nPress Enter to close...")
input()
