"""
Photobooth QR Automation System
===============================
Monitors a folder for new photos and displays a popup with
the photo preview and a QR code linking to Google Drive.

Features:
- Real-time file monitoring using watchdog
- QR code generation pointing to Google Drive
- Topmost borderless popup window
- Multi-threaded for handling rapid photo sequences
- File stability checking for large DSLR photos

Author: Photobooth Automation
"""

import os
import sys
import time
import threading
import queue
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

# Third-party imports
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from PIL import Image, ImageTk
import qrcode
import tkinter as tk
from tkinter import font as tkfont

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION - Modify these settings as needed
# ============================================================================

# Folder to monitor for new photos (Google Drive for Desktop sync folder)
WATCH_FOLDER = r"C:\Photobooth\Outputs"

# Time in seconds before the popup automatically closes
QR_DISPLAY_TIME = 30

# Your Google Drive shared folder ID (from the folder's shareable link)
# Example: If your link is https://drive.google.com/drive/folders/ABC123xyz
# Then DRIVE_FOLDER_ID = "ABC123xyz"
DRIVE_FOLDER_ID = "YOUR_GOOGLE_DRIVE_FOLDER_ID_HERE"

# Supported image extensions
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# File stability settings (for DSLR large files)
FILE_STABILITY_CHECKS = 3      # Number of consecutive size checks
FILE_CHECK_INTERVAL = 0.3      # Seconds between checks
MAX_WAIT_TIME = 10             # Maximum seconds to wait for file stability

# UI Configuration
WINDOW_WIDTH = 950
WINDOW_HEIGHT = 550
PHOTO_SIZE = (420, 420)
QR_SIZE = 320
BACKGROUND_COLOR = "#0d1117"
ACCENT_COLOR = "#161b22"
TEXT_COLOR = "#f0f6fc"
HEADER_COLOR = "#58a6ff"
BORDER_COLOR = "#30363d"
SUCCESS_COLOR = "#238636"

# ============================================================================
# FILE STABILITY CHECKER
# ============================================================================

def wait_for_file_stability(file_path: Path, 
                            checks: int = FILE_STABILITY_CHECKS,
                            interval: float = FILE_CHECK_INTERVAL,
                            max_wait: float = MAX_WAIT_TIME) -> bool:
    """
    Wait until a file is fully written by checking if its size remains stable.
    
    This is crucial for DSLR cameras that write large files - we need to wait
    until the camera/software has finished writing before we try to open the file.
    
    Args:
        file_path: Path to the file to check
        checks: Number of consecutive stable size readings required
        interval: Time between size checks in seconds
        max_wait: Maximum time to wait in seconds
        
    Returns:
        True if file is stable and readable, False if timed out or error
    """
    start_time = time.time()
    last_size = -1
    stable_count = 0
    
    while time.time() - start_time < max_wait:
        try:
            if not file_path.exists():
                logger.warning(f"File disappeared: {file_path.name}")
                return False
                
            current_size = file_path.stat().st_size
            
            # Check if file is empty (still being created)
            if current_size == 0:
                time.sleep(interval)
                continue
            
            # Check if size is stable
            if current_size == last_size:
                stable_count += 1
                if stable_count >= checks:
                    # Final check: try to open the file
                    try:
                        with open(file_path, 'rb') as f:
                            f.read(1024)  # Read first 1KB to verify access
                        logger.debug(f"File stable after {time.time() - start_time:.2f}s: {file_path.name}")
                        return True
                    except (IOError, PermissionError):
                        stable_count = 0  # Reset if file is still locked
            else:
                stable_count = 0
                
            last_size = current_size
            time.sleep(interval)
            
        except Exception as e:
            logger.error(f"Error checking file stability: {e}")
            time.sleep(interval)
    
    logger.warning(f"Timeout waiting for file: {file_path.name}")
    return False


# ============================================================================
# GOOGLE DRIVE URL HELPER
# ============================================================================

def get_drive_url(filename: str) -> str:
    """
    Generate a Google Drive direct download/view URL for a file.
    
    IMPORTANT: For this to work, you must:
    1. Have Google Drive for Desktop installed and syncing the WATCH_FOLDER
    2. Share the folder publicly (or with anyone with the link)
    3. Set the correct DRIVE_FOLDER_ID above
    
    Args:
        filename: The name of the file (e.g., "photo_001.jpg")
    
    Returns:
        A Google Drive URL that points to the file
    
    TODO: You may need to customize this function based on your setup.
    Options include:
    - Direct file ID lookup via Google Drive API
    - Using a web service to resolve the URL
    - Pre-configured URL patterns
    """
    # Option 1: Link to the shared folder (user can find their file)
    # This is the simplest approach that works without API setup
    folder_url = f"https://drive.google.com/drive/folders/{DRIVE_FOLDER_ID}"
    
    # Option 2: If you implement file ID lookup, use direct file URL:
    # file_url = f"https://drive.google.com/file/d/{file_id}/view"
    
    # Option 3: Direct download link (requires file_id):
    # download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    return folder_url


# ============================================================================
# QR CODE GENERATOR
# ============================================================================

def generate_qr_code(data: str, size: int = QR_SIZE) -> Image.Image:
    """
    Generate a QR code image from the given data.
    
    Args:
        data: The URL or text to encode in the QR code
        size: The desired size of the QR code image
    
    Returns:
        PIL Image object containing the QR code
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill_color="#1a1a2e", back_color="white")
    qr_image = qr_image.convert('RGB')
    qr_image = qr_image.resize((size, size), Image.Resampling.LANCZOS)
    
    return qr_image


# ============================================================================
# POPUP WINDOW CLASS
# ============================================================================

class PhotoPopup:
    """
    A topmost borderless window that displays a photo preview and QR code.
    Auto-closes after the configured display time.
    
    Note: Uses Toplevel when a root window exists, Tk otherwise.
    This allows multiple popups to coexist properly.
    """
    
    # Class-level lock for thread safety
    _tk_lock = threading.Lock()
    _popup_count = 0
    
    def __init__(self, image_path: str, qr_url: str, display_time: int = QR_DISPLAY_TIME):
        self.image_path = image_path
        self.qr_url = qr_url
        self.display_time = display_time
        self.root: Optional[tk.Tk] = None
        self.window: Optional[tk.Toplevel] = None
        self.countdown = display_time
        self.countdown_label: Optional[tk.Label] = None
        self._photo_image = None  # Keep reference to prevent garbage collection
        self._qr_image = None     # Keep reference to prevent garbage collection
        
    def show(self):
        """Create and display the popup window."""
        with PhotoPopup._tk_lock:
            PhotoPopup._popup_count += 1
            popup_id = PhotoPopup._popup_count
        
        # Create new Tk instance for this popup (each in its own thread)
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        
        # Create Toplevel window for the actual popup
        self.window = tk.Toplevel(self.root)
        self.window.title(f"Photobooth - Scan to Download")
        
        # Make window topmost and borderless
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)
        
        # Set window size and center on screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Offset each popup slightly so they don't overlap exactly
        offset = ((popup_id - 1) % 5) * 30
        x = (screen_width - WINDOW_WIDTH) // 2 + offset
        y = (screen_height - WINDOW_HEIGHT) // 2 + offset
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        
        # Set background color
        self.window.configure(bg=BACKGROUND_COLOR)
        
        # Build the UI
        self._build_ui()
        
        # Start countdown timer
        self._start_countdown()
        
        # Allow clicking anywhere to close
        self.window.bind('<Button-1>', lambda e: self._close())
        self.window.bind('<Escape>', lambda e: self._close())
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self._close)
        
        # Run the window
        self.root.mainloop()
    
    def _build_ui(self):
        """Build the popup user interface."""
        # Outer border frame
        border_frame = tk.Frame(self.window, bg=BORDER_COLOR, padx=2, pady=2)
        border_frame.pack(fill=tk.BOTH, expand=True)
        
        # Main container with padding
        main_frame = tk.Frame(border_frame, bg=BACKGROUND_COLOR, padx=35, pady=25)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        header_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Main header
        header_font = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        header_label = tk.Label(
            header_frame,
            text="📸 Scan to Download",
            font=header_font,
            fg=HEADER_COLOR,
            bg=BACKGROUND_COLOR
        )
        header_label.pack()
        
        # Subtitle
        subtitle_font = tkfont.Font(family="Segoe UI", size=12)
        subtitle_label = tk.Label(
            header_frame,
            text="Your photo is ready! Scan the QR code with your phone.",
            font=subtitle_font,
            fg="#8b949e",
            bg=BACKGROUND_COLOR
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Content frame (photo on left, QR on right)
        content_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Photo preview with border
        photo_outer = tk.Frame(content_frame, bg=BORDER_COLOR, padx=3, pady=3)
        photo_outer.pack(side=tk.LEFT, padx=(0, 30))
        
        photo_frame = tk.Frame(photo_outer, bg=ACCENT_COLOR, padx=12, pady=12)
        photo_frame.pack()
        
        photo_image = self._load_photo()
        photo_label = tk.Label(photo_frame, image=photo_image, bg=ACCENT_COLOR)
        photo_label.image = photo_image  # Keep reference
        photo_label.pack()
        
        # Photo filename with icon
        filename = Path(self.image_path).name
        # Truncate long filenames
        display_name = filename if len(filename) <= 35 else filename[:32] + "..."
        name_font = tkfont.Font(family="Segoe UI", size=10)
        name_label = tk.Label(
            photo_frame,
            text=f"📄 {display_name}",
            font=name_font,
            fg="#8b949e",
            bg=ACCENT_COLOR
        )
        name_label.pack(pady=(10, 0))
        
        # Right side - QR code section
        qr_frame = tk.Frame(content_frame, bg=BACKGROUND_COLOR)
        qr_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # QR code with white background frame
        qr_container = tk.Frame(qr_frame, bg="white", padx=10, pady=10)
        qr_container.pack(pady=(0, 15))
        
        qr_image = self._generate_qr()
        qr_label = tk.Label(qr_container, image=qr_image, bg="white")
        qr_label.image = qr_image  # Keep reference
        qr_label.pack()
        
        # Instructions with icon
        instruction_font = tkfont.Font(family="Segoe UI", size=13)
        instruction_label = tk.Label(
            qr_frame,
            text="📱 Point your camera at the QR code",
            font=instruction_font,
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            justify=tk.CENTER
        )
        instruction_label.pack(pady=(0, 8))
        
        # Secondary instruction
        sub_instruction_font = tkfont.Font(family="Segoe UI", size=11)
        sub_instruction = tk.Label(
            qr_frame,
            text="Opens in Google Drive for easy download",
            font=sub_instruction_font,
            fg="#8b949e",
            bg=BACKGROUND_COLOR
        )
        sub_instruction.pack()
        
        # Footer with countdown
        footer_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        # Divider line
        divider = tk.Frame(footer_frame, bg=BORDER_COLOR, height=1)
        divider.pack(fill=tk.X, pady=(0, 12))
        
        # Countdown timer
        countdown_font = tkfont.Font(family="Segoe UI", size=10)
        self.countdown_label = tk.Label(
            footer_frame,
            text=f"⏱ Closing in {self.countdown}s  •  Click anywhere or press ESC to close",
            font=countdown_font,
            fg="#6e7681",
            bg=BACKGROUND_COLOR
        )
        self.countdown_label.pack()
    
    def _load_photo(self) -> ImageTk.PhotoImage:
        """Load and resize the photo for preview."""
        try:
            img = Image.open(self.image_path)
            img.thumbnail(PHOTO_SIZE, Image.Resampling.LANCZOS)
            self._photo_image = ImageTk.PhotoImage(img, master=self.root)
            return self._photo_image
        except Exception as e:
            logger.error(f"Error loading photo: {e}")
            # Create a placeholder if image fails to load
            placeholder = Image.new('RGB', PHOTO_SIZE, color='#333333')
            self._photo_image = ImageTk.PhotoImage(placeholder, master=self.root)
            return self._photo_image
    
    def _generate_qr(self) -> ImageTk.PhotoImage:
        """Generate QR code image."""
        qr_img = generate_qr_code(self.qr_url)
        self._qr_image = ImageTk.PhotoImage(qr_img, master=self.root)
        return self._qr_image
    
    def _start_countdown(self):
        """Start the auto-close countdown."""
        self._update_countdown()
    
    def _update_countdown(self):
        """Update countdown display and close when finished."""
        if self.window is None or self.root is None:
            return
            
        if self.countdown <= 0:
            self._close()
            return
        
        try:
            if self.countdown_label and self.countdown_label.winfo_exists():
                self.countdown_label.config(
                    text=f"⏱ Closing in {self.countdown}s  •  Click anywhere or press ESC to close"
                )
            
            self.countdown -= 1
            self.root.after(1000, self._update_countdown)
        except tk.TclError:
            # Window was destroyed
            pass
    
    def _close(self):
        """Close the popup window."""
        try:
            if self.window:
                self.window.destroy()
                self.window = None
            if self.root:
                self.root.quit()
                self.root.destroy()
                self.root = None
        except tk.TclError:
            pass  # Window already destroyed


# ============================================================================
# FILE WATCHER
# ============================================================================

class PhotoEventHandler(FileSystemEventHandler):
    """
    Handles file system events for new photos.
    Puts detected photos into a queue for processing.
    """
    
    def __init__(self, photo_queue: queue.Queue):
        super().__init__()
        self.photo_queue = photo_queue
        self.processed_files = set()
        self.lock = threading.Lock()
    
    def on_created(self, event: FileCreatedEvent):
        """Called when a file is created in the watched folder."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Check if it's a supported image file
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return
        
        # Avoid processing the same file multiple times
        with self.lock:
            if str(file_path) in self.processed_files:
                return
            self.processed_files.add(str(file_path))
        
        logger.info(f"📷 New photo detected: {file_path.name}")
        
        # Process in a thread to not block the file watcher
        threading.Thread(
            target=self._process_new_file,
            args=(file_path,),
            daemon=True
        ).start()
    
    def _process_new_file(self, file_path: Path):
        """Process a new file after waiting for it to be fully written."""
        # Wait for file to be fully written (crucial for DSLR large files)
        logger.debug(f"Waiting for file stability: {file_path.name}")
        
        if wait_for_file_stability(file_path):
            # Verify it's a valid image
            try:
                with Image.open(file_path) as img:
                    img.verify()  # Verify image integrity
                logger.info(f"✅ File ready: {file_path.name}")
                self.photo_queue.put(str(file_path))
            except Exception as e:
                logger.error(f"❌ Invalid image file: {file_path.name} - {e}")
                with self.lock:
                    self.processed_files.discard(str(file_path))
        else:
            logger.error(f"❌ File not accessible: {file_path.name}")
            with self.lock:
                self.processed_files.discard(str(file_path))


class PhotoboothWatcher:
    """
    Main watcher class that monitors the folder and spawns popup windows.
    """
    
    def __init__(self, watch_folder: str):
        self.watch_folder = Path(watch_folder)
        self.photo_queue: queue.Queue = queue.Queue()
        self.observer: Optional[Observer] = None
        self.running = False
    
    def start(self):
        """Start watching the folder for new photos."""
        # Ensure watch folder exists
        if not self.watch_folder.exists():
            logger.info(f"Creating watch folder: {self.watch_folder}")
            self.watch_folder.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "═"*65)
        print("  📸 PHOTOBOOTH QR AUTOMATION SYSTEM")
        print("═"*65)
        print(f"  📁 Watch Folder:  {self.watch_folder}")
        print(f"  ⏱  Display Time:  {QR_DISPLAY_TIME} seconds")
        drive_id_display = f"{DRIVE_FOLDER_ID[:25]}..." if len(DRIVE_FOLDER_ID) > 25 else DRIVE_FOLDER_ID
        print(f"  ☁️  Drive Folder:  {drive_id_display}")
        print("─"*65)
        print("  ✓ File stability checking enabled")
        print("  ✓ Multi-threaded popup handling")
        print("  ✓ Supports JPG, JPEG, PNG formats")
        print("═"*65)
        print("  🟢 READY - Waiting for new photos...")
        print("  Press Ctrl+C to stop")
        print("═"*65 + "\n")
        
        # Set up the file watcher
        event_handler = PhotoEventHandler(self.photo_queue)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_folder), recursive=False)
        self.observer.start()
        
        self.running = True
        
        # Start the photo processor in the main thread
        self._process_photos()
    
    def _process_photos(self):
        """Process photos from the queue and display popups."""
        try:
            while self.running:
                try:
                    # Wait for a photo with timeout (allows checking running flag)
                    photo_path = self.photo_queue.get(timeout=1.0)
                    self._show_popup(photo_path)
                except queue.Empty:
                    continue
        except KeyboardInterrupt:
            print("\n")
            logger.info("🛑 Stopping photobooth watcher...")
            self.stop()
    
    def _show_popup(self, photo_path: str):
        """
        Show a popup for the given photo.
        Runs in a separate thread to not block the file watcher.
        """
        filename = Path(photo_path).name
        qr_url = get_drive_url(filename)
        
        logger.info(f"✨ Displaying popup for: {filename}")
        logger.debug(f"   QR URL: {qr_url}")
        
        # Run popup in a separate thread
        popup_thread = threading.Thread(
            target=self._run_popup,
            args=(photo_path, qr_url),
            daemon=True
        )
        popup_thread.start()
    
    def _run_popup(self, photo_path: str, qr_url: str):
        """Run the popup window (called in separate thread)."""
        try:
            popup = PhotoPopup(photo_path, qr_url)
            popup.show()
            logger.debug(f"Popup closed for: {Path(photo_path).name}")
        except Exception as e:
            logger.error(f"❌ Error showing popup: {e}")
    
    def stop(self):
        """Stop the watcher."""
        self.running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
        logger.info("👋 Photobooth watcher stopped. Goodbye!")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the application."""
    print("\n🚀 Starting Photobooth QR Automation System...")
    
    # Check if watch folder path is configured
    if WATCH_FOLDER == r"C:\Photobooth\Outputs":
        logger.warning("Using default watch folder path.")
        logger.warning(f"Current setting: {WATCH_FOLDER}")
        logger.warning("Edit WATCH_FOLDER in the script to change this.\n")
    
    if DRIVE_FOLDER_ID == "YOUR_GOOGLE_DRIVE_FOLDER_ID_HERE":
        logger.warning("⚠️  Google Drive folder ID not configured!")
        logger.warning("QR codes will point to a placeholder URL.")
        logger.warning("Edit DRIVE_FOLDER_ID in the script to fix this.\n")
    
    # Start the watcher
    watcher = PhotoboothWatcher(WATCH_FOLDER)
    
    try:
        watcher.start()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

