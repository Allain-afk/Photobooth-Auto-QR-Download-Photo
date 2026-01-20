"""
Professional Photobooth Application
Similar to DSLRBooth - A complete photobooth software solution

Features:
- Camera control (DSLR & Webcam)
- Live preview
- Touch-screen interface
- Photo templates & overlays
- Countdown timer
- Print functionality
- Email & social sharing
- Professional UI
"""

import tkinter as tk
from tkinter import messagebox
import sys
from pathlib import Path

# Import modules
from ui.main_window import PhotoboothApp
from core.camera_manager import CameraManager
from core.settings_manager import SettingsManager
from utils.logger import setup_logger

logger = setup_logger()


def main():
    """Main entry point for the photobooth application."""
    try:
        logger.info("=" * 60)
        logger.info("PHOTOBOOTH PRO - Starting Application")
        logger.info("=" * 60)
        
        # Initialize settings
        settings = SettingsManager()
        
        # Initialize camera manager
        camera = CameraManager(settings)
        
        # Create main application window
        root = tk.Tk()
        app = PhotoboothApp(root, camera, settings)
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        messagebox.showerror("Error", f"Application error:\n{e}")
        sys.exit(1)
    finally:
        logger.info("Application closed")


if __name__ == "__main__":
    main()
