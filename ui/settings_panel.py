"""
Settings Panel - Admin interface for configuration
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
from pathlib import Path


class SettingsPanel(tk.Toplevel):
    """Settings configuration panel."""
    
    def __init__(self, parent, settings, camera):
        super().__init__(parent)
        self.settings = settings
        self.camera = camera
        
        self.title("Photobooth Settings")
        self.geometry("900x700")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self._create_ui()
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
    
    def _create_ui(self):
        """Create settings UI."""
        # Header
        header = tk.Label(
            self,
            text="⚙️ Settings",
            font=tkfont.Font(family="Arial", size=24, weight="bold"),
            bg='#f0f0f0',
            fg='#333333'
        )
        header.pack(fill=tk.X, pady=10)
        
        # Notebook for tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        self._create_camera_tab(notebook)
        self._create_display_tab(notebook)
        self._create_photo_tab(notebook)
        self._create_print_tab(notebook)
        self._create_advanced_tab(notebook)
        
        # Buttons
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(
            button_frame,
            text="Save & Close",
            command=self._save_and_close,
            bg='#4CAF50',
            fg='white',
            font=tkfont.Font(family="Arial", size=12, weight="bold"),
            width=15,
            height=2,
            relief=tk.FLAT,
            cursor='hand2'
        ).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=self.destroy,
            bg='#f44336',
            fg='white',
            font=tkfont.Font(family="Arial", size=12, weight="bold"),
            width=15,
            height=2,
            relief=tk.FLAT,
            cursor='hand2'
        ).pack(side=tk.RIGHT, padx=5)
    
    def _create_camera_tab(self, notebook):
        """Camera settings tab."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Camera")
        
        # Camera type
        tk.Label(tab, text="Camera Type:", font=("Arial", 11, "bold")).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        camera_type_var = tk.StringVar(value=self.settings.get('camera_type'))
        ttk.Radiobutton(
            tab, text="Webcam", variable=camera_type_var, value="webcam"
        ).grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Radiobutton(
            tab, text="DSLR (gPhoto2)", variable=camera_type_var, value="dslr"
        ).grid(row=0, column=2, sticky=tk.W, padx=10)
        
        self.camera_type_var = camera_type_var
        
        # Resolution
        tk.Label(tab, text="Resolution:", font=("Arial", 11, "bold")).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        width_var = tk.StringVar(value=str(self.settings.get('camera_width')))
        height_var = tk.StringVar(value=str(self.settings.get('camera_height')))
        
        tk.Entry(tab, textvariable=width_var, width=10).grid(row=1, column=1, padx=5)
        tk.Label(tab, text="x").grid(row=1, column=2)
        tk.Entry(tab, textvariable=height_var, width=10).grid(row=1, column=3, padx=5)
        
        self.width_var = width_var
        self.height_var = height_var
    
    def _create_display_tab(self, notebook):
        """Display settings tab."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Display")
        
        # Fullscreen
        fullscreen_var = tk.BooleanVar(value=self.settings.get('fullscreen'))
        tk.Checkbutton(
            tab,
            text="Fullscreen Mode",
            variable=fullscreen_var,
            font=("Arial", 11)
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.fullscreen_var = fullscreen_var
        
        # Event name
        tk.Label(tab, text="Event Name:", font=("Arial", 11, "bold")).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        event_name_var = tk.StringVar(value=self.settings.get('event_name'))
        tk.Entry(tab, textvariable=event_name_var, width=40).grid(
            row=1, column=1, columnspan=2, sticky=tk.W, padx=10
        )
        self.event_name_var = event_name_var
    
    def _create_photo_tab(self, notebook):
        """Photo settings tab."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Photo")
        
        # Save folder
        tk.Label(tab, text="Save Folder:", font=("Arial", 11, "bold")).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        folder_var = tk.StringVar(value=self.settings.get('save_folder'))
        tk.Entry(tab, textvariable=folder_var, width=40).grid(
            row=0, column=1, padx=10
        )
        tk.Button(
            tab, text="Browse...", command=lambda: self._browse_folder(folder_var)
        ).grid(row=0, column=2, padx=5)
        self.folder_var = folder_var
        
        # Quality
        tk.Label(tab, text="JPEG Quality:", font=("Arial", 11, "bold")).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        quality_var = tk.IntVar(value=self.settings.get('photo_quality'))
        tk.Scale(
            tab, from_=50, to=100, orient=tk.HORIZONTAL,
            variable=quality_var, length=300
        ).grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=10)
        self.quality_var = quality_var
        
        # Countdown
        tk.Label(tab, text="Countdown (seconds):", font=("Arial", 11, "bold")).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        countdown_var = tk.IntVar(value=self.settings.get('countdown_seconds'))
        tk.Spinbox(
            tab, from_=0, to=10, textvariable=countdown_var, width=10
        ).grid(row=2, column=1, sticky=tk.W, padx=10)
        self.countdown_var = countdown_var
    
    def _create_print_tab(self, notebook):
        """Print settings tab."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Print & Email")
        
        # Enable printing
        print_var = tk.BooleanVar(value=self.settings.get('enable_print'))
        tk.Checkbutton(
            tab, text="Enable Printing", variable=print_var, font=("Arial", 11)
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.print_var = print_var
        
        # Enable email
        email_var = tk.BooleanVar(value=self.settings.get('enable_email'))
        tk.Checkbutton(
            tab, text="Enable Email Sharing", variable=email_var, font=("Arial", 11)
        ).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.email_var = email_var
    
    def _create_advanced_tab(self, notebook):
        """Advanced settings tab."""
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Advanced")
        
        # Overlay
        overlay_var = tk.BooleanVar(value=self.settings.get('use_overlay'))
        tk.Checkbutton(
            tab, text="Use Photo Overlay/Template", variable=overlay_var, font=("Arial", 11)
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.overlay_var = overlay_var
        
        tk.Label(tab, text="Overlay Image:", font=("Arial", 11)).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        overlay_path_var = tk.StringVar(value=self.settings.get('overlay_path'))
        tk.Entry(tab, textvariable=overlay_path_var, width=40).grid(
            row=1, column=1, padx=10
        )
        tk.Button(
            tab, text="Browse...", command=lambda: self._browse_image(overlay_path_var)
        ).grid(row=1, column=2, padx=5)
        self.overlay_path_var = overlay_path_var
    
    def _browse_folder(self, var):
        """Browse for folder."""
        folder = filedialog.askdirectory(initialdir=var.get())
        if folder:
            var.set(folder)
    
    def _browse_image(self, var):
        """Browse for image file."""
        file = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if file:
            var.set(file)
    
    def _save_and_close(self):
        """Save settings and close."""
        try:
            self.settings.update(
                camera_type=self.camera_type_var.get(),
                camera_width=int(self.width_var.get()),
                camera_height=int(self.height_var.get()),
                fullscreen=self.fullscreen_var.get(),
                event_name=self.event_name_var.get(),
                save_folder=self.folder_var.get(),
                photo_quality=self.quality_var.get(),
                countdown_seconds=self.countdown_var.get(),
                enable_print=self.print_var.get(),
                enable_email=self.email_var.get(),
                use_overlay=self.overlay_var.get(),
                overlay_path=self.overlay_path_var.get(),
            )
            
            messagebox.showinfo("Success", "Settings saved!\n\nRestart for some changes to take effect.")
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings:\n{e}")
