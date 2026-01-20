"""
Settings Manager - Handles application settings
"""

import json
from pathlib import Path
from typing import Any
from utils.logger import get_logger

logger = get_logger(__name__)

CONFIG_FILE = "photobooth_settings.json"

DEFAULT_SETTINGS = {
    # Camera settings
    "camera_type": "webcam",  # 'webcam' or 'dslr'
    "webcam_index": 0,
    "camera_width": 1920,
    "camera_height": 1080,
    
    # Display settings
    "fullscreen": True,
    "screen_width": 1920,
    "screen_height": 1080,
    
    # Photo settings
    "photo_format": "jpg",
    "photo_quality": 95,
    "save_folder": "photos",
    
    # UI settings
    "countdown_seconds": 3,
    "review_time_seconds": 5,
    "idle_timeout_seconds": 30,
    
    # Template settings
    "use_overlay": False,
    "overlay_path": "",
    
    # Print settings
    "enable_print": False,
    "printer_name": "",
    "print_copies": 1,
    "auto_print": False,
    
    # Email settings
    "enable_email": False,
    "smtp_server": "",
    "smtp_port": 587,
    "smtp_username": "",
    "smtp_password": "",
    
    # Branding
    "event_name": "Photo Booth",
    "show_logo": False,
    "logo_path": "",
    
    # Effects
    "enable_flash": True,
    "enable_sound": True,
    "sound_volume": 0.7,
}


class SettingsManager:
    """Manages application settings."""
    
    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = Path(config_file)
        self.settings = self.load()
    
    def load(self) -> dict:
        """Load settings from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**DEFAULT_SETTINGS, **settings}
            except Exception as e:
                logger.error(f"Error loading settings: {e}")
                return DEFAULT_SETTINGS.copy()
        else:
            # Create default settings file
            self.save(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS.copy()
    
    def save(self, settings: dict = None):
        """Save settings to file."""
        if settings is not None:
            self.settings = settings
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            logger.info("Settings saved")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value."""
        self.settings[key] = value
    
    def update(self, **kwargs):
        """Update multiple settings."""
        self.settings.update(kwargs)
        self.save()
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = DEFAULT_SETTINGS.copy()
        self.save()
