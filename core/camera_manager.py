"""
Camera Manager - Handles all camera operations
Supports both webcam and DSLR cameras
"""

import cv2
import numpy as np
from PIL import Image
import threading
import time
from typing import Optional, Callable
from utils.logger import get_logger

# Optional DSLR support (requires gphoto2)
try:
    import gphoto2 as gp
    GPHOTO2_AVAILABLE = True
except ImportError:
    GPHOTO2_AVAILABLE = False
    gp = None

logger = get_logger(__name__)


class CameraManager:
    """Manages camera operations for webcam and DSLR."""
    
    def __init__(self, settings):
        self.settings = settings
        self.camera = None
        self.camera_type = settings.get('camera_type', 'webcam')  # 'webcam' or 'dslr'
        self.is_running = False
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.preview_callback = None
        
        # DSLR specific
        self.gp_camera = None
        self.gp_context = None
        
    def initialize(self) -> bool:
        """Initialize the camera based on settings."""
        try:
            if self.camera_type == 'webcam':
                return self._initialize_webcam()
            else:
                return self._initialize_dslr()
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            return False
    
    def _initialize_webcam(self) -> bool:
        """Initialize webcam."""
        try:
            camera_index = self.settings.get('webcam_index', 0)
            self.camera = cv2.VideoCapture(camera_index)
            
            if not self.camera.isOpened():
                logger.error("Failed to open webcam")
                return False
            
            # Set resolution
            width = self.settings.get('camera_width', 1920)
            height = self.settings.get('camera_height', 1080)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
            logger.info(f"Webcam initialized: {width}x{height}")
            return True
            
        except Exception as e:
            logger.error(f"Webcam initialization error: {e}")
            return False
    
    def _initialize_dslr(self) -> bool:
        """Initialize DSLR camera using gphoto2."""
        if not GPHOTO2_AVAILABLE:
            logger.warning("gphoto2 not installed. Falling back to webcam...")
            logger.info("Install gphoto2 for DSLR support: pip install gphoto2")
            self.camera_type = 'webcam'
            return self._initialize_webcam()
        
        try:
            self.gp_context = gp.Context()
            self.gp_camera = gp.Camera()
            self.gp_camera.init(self.gp_context)
            
            logger.info("DSLR camera initialized")
            return True
            
        except Exception as e:
            logger.error(f"DSLR initialization error: {e}")
            logger.info("Falling back to webcam...")
            self.camera_type = 'webcam'
            return self._initialize_webcam()
    
    def start_preview(self, callback: Optional[Callable] = None):
        """Start live preview."""
        self.preview_callback = callback
        self.is_running = True
        
        if self.camera_type == 'webcam':
            threading.Thread(target=self._webcam_preview_loop, daemon=True).start()
        else:
            threading.Thread(target=self._dslr_preview_loop, daemon=True).start()
    
    def _webcam_preview_loop(self):
        """Webcam preview loop."""
        while self.is_running:
            ret, frame = self.camera.read()
            if ret:
                # Convert BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                with self.frame_lock:
                    self.current_frame = frame
                
                if self.preview_callback:
                    self.preview_callback(frame)
            
            time.sleep(0.033)  # ~30 FPS
    
    def _dslr_preview_loop(self):
        """DSLR preview loop."""
        while self.is_running:
            try:
                camera_file = self.gp_camera.capture_preview(self.gp_context)
                file_data = camera_file.get_data_and_size()
                
                # Convert to numpy array
                image = Image.frombytes('RGB', (0, 0), file_data)
                frame = np.array(image)
                
                with self.frame_lock:
                    self.current_frame = frame
                
                if self.preview_callback:
                    self.preview_callback(frame)
                    
            except Exception as e:
                logger.error(f"DSLR preview error: {e}")
                time.sleep(0.1)
    
    def capture_photo(self) -> Optional[np.ndarray]:
        """Capture a photo."""
        try:
            if self.camera_type == 'webcam':
                return self._capture_webcam()
            else:
                return self._capture_dslr()
        except Exception as e:
            logger.error(f"Photo capture error: {e}")
            return None
    
    def _capture_webcam(self) -> Optional[np.ndarray]:
        """Capture photo from webcam."""
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            logger.info("Photo captured from webcam")
            return frame
        return None
    
    def _capture_dslr(self) -> Optional[np.ndarray]:
        """Capture photo from DSLR."""
        if not GPHOTO2_AVAILABLE:
            logger.error("gphoto2 not available")
            return None
        
        try:
            import io
            
            file_path = self.gp_camera.capture(gp.GP_CAPTURE_IMAGE, self.gp_context)
            camera_file = self.gp_camera.file_get(
                file_path.folder, file_path.name,
                gp.GP_FILE_TYPE_NORMAL, self.gp_context
            )
            
            file_data = camera_file.get_data_and_size()
            image = Image.open(io.BytesIO(file_data))
            frame = np.array(image)
            
            logger.info("Photo captured from DSLR")
            return frame
            
        except Exception as e:
            logger.error(f"DSLR capture error: {e}")
            return None
    
    def get_current_frame(self) -> Optional[np.ndarray]:
        """Get the current preview frame."""
        with self.frame_lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def stop_preview(self):
        """Stop the preview."""
        self.is_running = False
    
    def release(self):
        """Release camera resources."""
        self.stop_preview()
        
        if self.camera_type == 'webcam' and self.camera:
            self.camera.release()
        elif self.camera_type == 'dslr' and self.gp_camera:
            try:
                self.gp_camera.exit(self.gp_context)
            except:
                pass
        
        logger.info("Camera released")
