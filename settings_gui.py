"""
Settings GUI for Photobooth QR System
Allows users to configure watch folder and Google Drive settings.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
from pathlib import Path
from config_manager import ConfigManager


class SettingsWindow:
    """Settings configuration window."""
    
    def __init__(self, config_manager: ConfigManager, on_save_callback=None):
        self.config = config_manager
        self.on_save_callback = on_save_callback
        self.window = None
        self.watch_folder_var = None
        self.drive_id_var = None
        self.display_time_var = None
        
    def show(self):
        """Display the settings window."""
        self.window = tk.Tk()
        self.window.title("Photobooth Settings")
        self.window.geometry("700x500")
        self.window.resizable(False, False)
        
        # Configure styling
        bg_color = "#f0f0f0"
        self.window.configure(bg=bg_color)
        
        # Main container
        main_frame = tk.Frame(self.window, bg=bg_color, padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        header = tk.Label(
            main_frame,
            text="⚙️ Photobooth Settings",
            font=header_font,
            bg=bg_color,
            fg="#2c3e50"
        )
        header.pack(pady=(0, 25))
        
        # Settings form
        self._create_form(main_frame, bg_color)
        
        # Buttons
        self._create_buttons(main_frame, bg_color)
        
        # Center window on screen
        self._center_window()
        
        # Make it topmost initially
        self.window.lift()
        self.window.focus_force()
        
        self.window.mainloop()
    
    def _create_form(self, parent, bg_color):
        """Create the settings form."""
        form_frame = tk.Frame(parent, bg=bg_color)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        label_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        entry_font = tkfont.Font(family="Segoe UI", size=10)
        help_font = tkfont.Font(family="Segoe UI", size=9)
        
        # Watch Folder
        tk.Label(
            form_frame,
            text="📁 Watch Folder (Where photos are saved):",
            font=label_font,
            bg=bg_color,
            fg="#34495e",
            anchor="w"
        ).pack(fill=tk.X, pady=(10, 5))
        
        folder_frame = tk.Frame(form_frame, bg=bg_color)
        folder_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.watch_folder_var = tk.StringVar(value=self.config.get("watch_folder", ""))
        folder_entry = tk.Entry(
            folder_frame,
            textvariable=self.watch_folder_var,
            font=entry_font,
            width=50
        )
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        browse_btn = tk.Button(
            folder_frame,
            text="Browse...",
            command=self._browse_folder,
            bg="#3498db",
            fg="white",
            font=entry_font,
            cursor="hand2",
            relief=tk.FLAT,
            padx=15
        )
        browse_btn.pack(side=tk.LEFT, padx=(10, 0), ipady=3)
        
        tk.Label(
            form_frame,
            text="This folder will be monitored for new .jpg and .png files",
            font=help_font,
            bg=bg_color,
            fg="#7f8c8d",
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 15))
        
        # Google Drive Folder ID
        tk.Label(
            form_frame,
            text="☁️ Google Drive Folder ID:",
            font=label_font,
            bg=bg_color,
            fg="#34495e",
            anchor="w"
        ).pack(fill=tk.X, pady=(10, 5))
        
        self.drive_id_var = tk.StringVar(value=self.config.get("drive_folder_id", ""))
        drive_entry = tk.Entry(
            form_frame,
            textvariable=self.drive_id_var,
            font=entry_font
        )
        drive_entry.pack(fill=tk.X, ipady=5, pady=(0, 5))
        
        help_text = (
            "Get this from your Google Drive shared folder URL:\n"
            "https://drive.google.com/drive/folders/YOUR_FOLDER_ID\n"
            "Make sure the folder is shared with 'Anyone with the link'"
        )
        tk.Label(
            form_frame,
            text=help_text,
            font=help_font,
            bg=bg_color,
            fg="#7f8c8d",
            anchor="w",
            justify=tk.LEFT
        ).pack(fill=tk.X, pady=(0, 15))
        
        # Display Time
        tk.Label(
            form_frame,
            text="⏱️ Auto-close time (seconds):",
            font=label_font,
            bg=bg_color,
            fg="#34495e",
            anchor="w"
        ).pack(fill=tk.X, pady=(10, 5))
        
        time_frame = tk.Frame(form_frame, bg=bg_color)
        time_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.display_time_var = tk.IntVar(value=self.config.get("qr_display_time", 30))
        time_spinbox = tk.Spinbox(
            time_frame,
            from_=5,
            to=300,
            textvariable=self.display_time_var,
            font=entry_font,
            width=10
        )
        time_spinbox.pack(side=tk.LEFT, ipady=3)
        
        tk.Label(
            time_frame,
            text="seconds before popup auto-closes",
            font=help_font,
            bg=bg_color,
            fg="#7f8c8d"
        ).pack(side=tk.LEFT, padx=(10, 0))
    
    def _create_buttons(self, parent, bg_color):
        """Create action buttons."""
        button_frame = tk.Frame(parent, bg=bg_color)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        button_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        
        # Save button
        save_btn = tk.Button(
            button_frame,
            text="💾 Save & Start",
            command=self._save_settings,
            bg="#27ae60",
            fg="white",
            font=button_font,
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.window.destroy,
            bg="#95a5a6",
            fg="white",
            font=button_font,
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        cancel_btn.pack(side=tk.RIGHT)
    
    def _browse_folder(self):
        """Open folder browser dialog."""
        current_folder = self.watch_folder_var.get()
        initial_dir = current_folder if Path(current_folder).exists() else str(Path.home())
        
        folder = filedialog.askdirectory(
            title="Select Photo Watch Folder",
            initialdir=initial_dir
        )
        
        if folder:
            self.watch_folder_var.set(folder)
    
    def _validate_settings(self) -> bool:
        """Validate settings before saving."""
        watch_folder = self.watch_folder_var.get().strip()
        drive_id = self.drive_id_var.get().strip()
        
        if not watch_folder:
            messagebox.showerror(
                "Validation Error",
                "Please specify a watch folder!"
            )
            return False
        
        if not drive_id:
            response = messagebox.askywarning(
                "Warning",
                "Google Drive Folder ID is empty. QR codes will not work properly.\n\n"
                "Continue anyway?",
                type=messagebox.OKCANCEL
            )
            if response != messagebox.OK:
                return False
        
        # Create watch folder if it doesn't exist
        folder_path = Path(watch_folder)
        if not folder_path.exists():
            response = messagebox.askyesno(
                "Create Folder",
                f"The folder doesn't exist:\n{watch_folder}\n\n"
                "Do you want to create it?"
            )
            if response:
                try:
                    folder_path.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"Could not create folder:\n{e}"
                    )
                    return False
            else:
                return False
        
        return True
    
    def _save_settings(self):
        """Save settings and close window."""
        if not self._validate_settings():
            return
        
        # Update configuration
        self.config.update(
            watch_folder=self.watch_folder_var.get().strip(),
            drive_folder_id=self.drive_id_var.get().strip(),
            qr_display_time=self.display_time_var.get()
        )
        
        messagebox.showinfo(
            "Settings Saved",
            "Configuration saved successfully!\n\nThe photobooth will now start monitoring."
        )
        
        # Call the callback if provided
        if self.on_save_callback:
            self.on_save_callback()
        
        self.window.destroy()
    
    def _center_window(self):
        """Center window on screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')


if __name__ == "__main__":
    # Test the settings window
    config = ConfigManager()
    settings = SettingsWindow(config)
    settings.show()
