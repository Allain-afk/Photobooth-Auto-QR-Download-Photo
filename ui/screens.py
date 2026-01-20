"""
Screen Components for Photobooth
Different screens: Start, Countdown, Review, etc.
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import threading
import time


class StartScreen(tk.Frame):
    """Start/Idle screen - Touch to begin."""
    
    def __init__(self, parent, settings, on_start):
        super().__init__(parent, bg='#1a1a2e')
        self.settings = settings
        self.on_start = on_start
        
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self._build_ui()
    
    def _build_ui(self):
        """Build the start screen UI."""
        # Event name/title
        event_name = self.settings.get('event_name', 'Photo Booth')
        title_font = tkfont.Font(family="Arial", size=80, weight="bold")
        
        title = tk.Label(
            self,
            text=event_name,
            font=title_font,
            fg='#00d4ff',
            bg='#1a1a2e'
        )
        title.pack(pady=(200, 50))
        
        # Instruction text
        instruction_font = tkfont.Font(family="Arial", size=40)
        instruction = tk.Label(
            self,
            text="TAP TO START",
            font=instruction_font,
            fg='#ffffff',
            bg='#1a1a2e'
        )
        instruction.pack(pady=30)
        
        # Animated button
        self.start_button = tk.Button(
            self,
            text="START",
            font=tkfont.Font(family="Arial", size=50, weight="bold"),
            bg='#00d4ff',
            fg='#000000',
            activebackground='#00b4df',
            activeforeground='#000000',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.on_start,
            width=15,
            height=2
        )
        self.start_button.pack(pady=50)
        
        # Make entire screen clickable
        self.bind('<Button-1>', lambda e: self.on_start())
        title.bind('<Button-1>', lambda e: self.on_start())
        instruction.bind('<Button-1>', lambda e: self.on_start())


class CountdownScreen(tk.Frame):
    """Countdown screen before photo capture."""
    
    def __init__(self, parent, settings, countdown_seconds, on_complete):
        super().__init__(parent, bg='#000000')
        self.settings = settings
        self.countdown_seconds = countdown_seconds
        self.on_complete = on_complete
        self.current_count = countdown_seconds
        
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self._build_ui()
        self._start_countdown()
    
    def _build_ui(self):
        """Build countdown UI."""
        # Instruction
        instruction_font = tkfont.Font(family="Arial", size=40)
        instruction = tk.Label(
            self,
            text="GET READY!",
            font=instruction_font,
            fg='#00d4ff',
            bg='#000000'
        )
        instruction.pack(pady=(150, 50))
        
        # Countdown number
        self.countdown_label = tk.Label(
            self,
            text=str(self.current_count),
            font=tkfont.Font(family="Arial", size=300, weight="bold"),
            fg='#ffffff',
            bg='#000000'
        )
        self.countdown_label.pack(expand=True)
    
    def _start_countdown(self):
        """Start the countdown timer."""
        threading.Thread(target=self._countdown_loop, daemon=True).start()
    
    def _countdown_loop(self):
        """Countdown loop."""
        for i in range(self.countdown_seconds, 0, -1):
            self.current_count = i
            self.countdown_label.config(text=str(i))
            
            # Flash effect on each count
            if i <= 3:
                self.countdown_label.config(fg='#ff6b6b')
                self.after(200, lambda: self.countdown_label.config(fg='#ffffff'))
            
            time.sleep(1)
        
        # Capture!
        self.countdown_label.config(text="SMILE!", fg='#00d4ff')
        time.sleep(0.3)
        self.on_complete()


class ReviewScreen(tk.Frame):
    """Photo review screen - Show captured photo with options."""
    
    def __init__(self, parent, settings, photo, on_print, on_email, on_done):
        super().__init__(parent, bg='#1a1a2e')
        self.settings = settings
        self.photo = photo
        self.on_print = on_print
        self.on_email = on_email
        self.on_done = on_done
        
        self.photo_image = None
        self.timeout_id = None
        
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self._build_ui()
        self._start_timeout()
    
    def _build_ui(self):
        """Build review screen UI."""
        # Header
        header_font = tkfont.Font(family="Arial", size=40, weight="bold")
        header = tk.Label(
            self,
            text="YOUR PHOTO!",
            font=header_font,
            fg='#00d4ff',
            bg='#1a1a2e'
        )
        header.pack(pady=30)
        
        # Photo display
        photo_frame = tk.Frame(self, bg='#ffffff', padx=5, pady=5)
        photo_frame.pack(pady=20)
        
        # Convert and display photo
        img = Image.fromarray(self.photo)
        img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(img)
        
        photo_label = tk.Label(photo_frame, image=self.photo_image, bg='#ffffff')
        photo_label.pack()
        
        # Buttons
        button_frame = tk.Frame(self, bg='#1a1a2e')
        button_frame.pack(pady=40)
        
        button_font = tkfont.Font(family="Arial", size=30, weight="bold")
        
        # Print button (if enabled)
        if self.settings.get('enable_print'):
            print_btn = tk.Button(
                button_frame,
                text="🖨️ PRINT",
                font=button_font,
                bg='#4CAF50',
                fg='#ffffff',
                activebackground='#45a049',
                command=lambda: self.on_print(self.photo),
                width=12,
                height=2,
                relief=tk.FLAT,
                cursor='hand2'
            )
            print_btn.pack(side=tk.LEFT, padx=20)
        
        # Email button (if enabled)
        if self.settings.get('enable_email'):
            email_btn = tk.Button(
                button_frame,
                text="📧 EMAIL",
                font=button_font,
                bg='#2196F3',
                fg='#ffffff',
                activebackground='#0b7dda',
                command=lambda: self.on_email(self.photo),
                width=12,
                height=2,
                relief=tk.FLAT,
                cursor='hand2'
            )
            email_btn.pack(side=tk.LEFT, padx=20)
        
        # Done button
        done_btn = tk.Button(
            button_frame,
            text="✓ DONE",
            font=button_font,
            bg='#00d4ff',
            fg='#000000',
            activebackground='#00b4df',
            command=self._finish,
            width=12,
            height=2,
            relief=tk.FLAT,
            cursor='hand2'
        )
        done_btn.pack(side=tk.LEFT, padx=20)
        
        # Timeout message
        review_time = self.settings.get('review_time_seconds', 5)
        timeout_msg = tk.Label(
            self,
            text=f"Returning to start in {review_time} seconds...",
            font=tkfont.Font(family="Arial", size=20),
            fg='#888888',
            bg='#1a1a2e'
        )
        timeout_msg.pack(side=tk.BOTTOM, pady=30)
    
    def _start_timeout(self):
        """Auto-return to start after timeout."""
        timeout_ms = self.settings.get('review_time_seconds', 5) * 1000
        self.timeout_id = self.after(timeout_ms, self._finish)
    
    def _finish(self):
        """Finish review and return to start."""
        if self.timeout_id:
            self.after_cancel(self.timeout_id)
        self.on_done()
