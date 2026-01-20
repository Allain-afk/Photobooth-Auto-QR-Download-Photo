"""
Configuration Manager for Photobooth QR System
Handles saving and loading settings from a JSON config file.
"""

import json
from pathlib import Path
from typing import Optional

CONFIG_FILE = "photobooth_config.json"

DEFAULT_CONFIG = {
    "watch_folder": r"C:\Photobooth\Outputs",
    "drive_folder_id": "",
    "qr_display_time": 30,
    "window_width": 950,
    "window_height": 550,
}


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = Path(config_file)
        self.config = self.load()
    
    def load(self) -> dict:
        """Load configuration from file, or create default if not exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**DEFAULT_CONFIG, **config}
            except Exception as e:
                print(f"Error loading config: {e}")
                return DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
    
    def save(self, config: Optional[dict] = None):
        """Save configuration to file."""
        if config is not None:
            self.config = config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value):
        """Set a configuration value."""
        self.config[key] = value
    
    def update(self, **kwargs):
        """Update multiple configuration values."""
        self.config.update(kwargs)
        self.save()
