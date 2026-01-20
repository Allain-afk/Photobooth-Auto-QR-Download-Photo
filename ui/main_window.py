"""
Main Window - Primary photobooth interface
Touch-friendly fullscreen interface
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
from typing import Optional
import threading
import time

from ui.settings_panel import SettingsPanel
from ui.screens import *
from utils.logger import get_logger

logger = get_logger(__name__)


class PhotoboothApp:
    """Main photobooth application window."""
    
    def __init__(self, root, camera, settings):
        self.root = root
        self.camera = camera
        self.settings = settings
        
        self.current_screen = None
        self.photo_image = None  # Keep reference for GC
        
        # Setup window
        self._setup_window()
        
        # Initialize camera
        if not self.camera.initialize():
            from tkinter import messagebox
            messagebox.showerror("Camera Error", 
                               "Failed to initialize camera!\n\nCheck connections and try again.")
            self.root.quit()
            return
        
        # Show start screen
        self.show_start_screen()
        
        # Start camera preview
        self.camera.start_preview(self._update_preview)
        
        logger.info("Photobooth application ready")
    
    def _setup_window(self):
        """Setup main window."""
        self.root.title("Photobooth Pro")
        
        # Fullscreen setup
        if self.settings.get('fullscreen'):
            self.root.attributes('-fullscreen', True)
            self.root.configure(cursor='none')  # Hide cursor in fullscreen
        else:
            width = self.settings.get('screen_width', 1920)
            height = self.settings.get('screen_height', 1080)
            self.root.geometry(f"{width}x{height}")
        
        self.root.configure(bg='#000000')
        
        # Escape key to exit fullscreen / quit
        self.root.bind('<Escape>', self._toggle_fullscreen)
        self.root.bind('<F11>', self._toggle_fullscreen)
        
        # Admin panel (Ctrl+S for settings)
        self.root.bind('<Control-s>', self._show_settings)
    
    def _toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode."""
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)
        if not current:
            self.root.configure(cursor='none')
        else:
            self.root.configure(cursor='')
    
    def _show_settings(self, event=None):
        """Show settings panel."""
        SettingsPanel(self.root, self.settings, self.camera)
    
    def show_start_screen(self):
        """Show the start/idle screen."""
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = StartScreen(
            self.root, 
            self.settings,
            on_start=self.start_capture_sequence
        )
    
    def start_capture_sequence(self):
        """Start the photo capture sequence."""
        logger.info("Starting capture sequence")
        
        # Show countdown screen
        if self.current_screen:
            self.current_screen.destroy()
        
        countdown_seconds = self.settings.get('countdown_seconds', 3)
        self.current_screen = CountdownScreen(
            self.root,
            self.settings,
            countdown_seconds,
            on_complete=self._capture_photo
        )
    
    def _capture_photo(self):
        """Capture the photo."""
        logger.info("Capturing photo...")
        
        # Flash effect if enabled
        if self.settings.get('enable_flash'):
            self._flash_effect()
        
        # Capture from camera
        photo = self.camera.capture_photo()
        
        if photo is None:
            logger.error("Failed to capture photo")
            self.show_start_screen()
            return
        
        # Apply overlay if enabled
        if self.settings.get('use_overlay'):
            photo = self._apply_overlay(photo)
        
        # Save photo
        self._save_photo(photo)
        
        # Show review screen
        self.show_review_screen(photo)
    
    def _flash_effect(self):
        """Show flash effect."""
        flash = tk.Frame(self.root, bg='white')
        flash.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.update()
        time.sleep(0.1)
        flash.destroy()
    
    def _apply_overlay(self, photo: np.ndarray) -> np.ndarray:
        """Apply overlay template to photo."""
        overlay_path = self.settings.get('overlay_path')
        if not overlay_path:
            return photo
        
        try:
            overlay = Image.open(overlay_path).convert('RGBA')
            photo_img = Image.fromarray(photo).convert('RGBA')
            
            # Resize overlay to match photo
            overlay = overlay.resize(photo_img.size, Image.Resampling.LANCZOS)
            
            # Composite
            result = Image.alpha_composite(photo_img, overlay)
            return np.array(result.convert('RGB'))
            
        except Exception as e:
            logger.error(f"Failed to apply overlay: {e}")
            return photo
    
    def _save_photo(self, photo: np.ndarray):
        """Save photo to disk."""
        from datetime import datetime
        from pathlib import Path
        
        save_folder = Path(self.settings.get('save_folder', 'photos'))
        save_folder.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        filepath = save_folder / filename
        
        # Convert numpy array to PIL Image and save
        img = Image.fromarray(photo)
        img.save(filepath, 'JPEG', quality=self.settings.get('photo_quality', 95))
        
        logger.info(f"Photo saved: {filepath}")
    
    def show_review_screen(self, photo: np.ndarray):
        """Show photo review screen."""
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = ReviewScreen(
            self.root,
            self.settings,
            photo,
            on_print=self._print_photo,
            on_email=self._email_photo,
            on_done=self.show_start_screen
        )
    
    def _print_photo(self, photo: np.ndarray):
        """Print the photo."""
        logger.info("Printing photo...")
        # TODO: Implement printing
        pass
    
    def _email_photo(self, photo: np.ndarray):
        """Email the photo."""
        logger.info("Emailing photo...")
        # TODO: Implement email
        pass
    
    def _update_preview(self, frame: np.ndarray):
        """Update preview callback from camera."""
        # This can be used for live preview if needed
        pass
    
    def cleanup(self):
        """Cleanup resources."""
        self.camera.release()
        logger.info("Application cleanup complete")
