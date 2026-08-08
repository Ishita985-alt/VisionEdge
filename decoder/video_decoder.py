"""
VisionEdge - Camera Manager

Handles camera initialization, frame capture,
camera status and resource cleanup.
"""

import cv2
import logging
from typing import Optional


class CameraManager:
    """Manages the system camera using OpenCV."""

    def __init__(self, camera_id: int = 0, width: int = 1280, height: int = 720):
        self.camera_id = camera_id
        self.width = width
        self.height = height

        self.camera: Optional[cv2.VideoCapture] = None
        self.is_running = False

        self.logger = logging.getLogger("VisionEdge.CameraManager")

    def start(self) -> bool:
        """Initialize and start the camera."""

        if self.is_running:
            self.logger.warning("Camera is already running.")
            return True

        self.logger.info("Starting camera %s...", self.camera_id)

        self.camera = cv2.VideoCapture(self.camera_id)

        if not self.camera.isOpened():
            self.logger.error("Unable to open camera %s.", self.camera_id)
            self.camera = None
            return False

        # Configure camera resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.is_running = True

        actual_width = int(
            self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        )
        actual_height = int(
            self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        self.logger.info(
            "Camera started successfully: %sx%s",
            actual_width,
            actual_height
        )

        return True

    def read_frame(self):
        """Capture a single frame from the camera."""

        if not self.is_running or self.camera is None:
            self.logger.warning("Camera is not running.")
            return None

        success, frame = self.camera.read()

        if not success:
            self.logger.error("Failed to capture camera frame.")
            return None

        return frame

    def is_available(self) -> bool:
        """Check whether the camera is available."""

        if self.camera is None:
            return False

        return self.camera.isOpened()

    def get_resolution(self):
        """Return the current camera resolution."""

        if not self.camera:
            return None

        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return width, height

    def stop(self):
        """Stop the camera and release resources."""

        if self.camera is not None:
            self.camera.release()

        self.camera = None
        self.is_running = False

        self.logger.info("Camera stopped.")

    def save_frame(self, frame, filename: str) -> bool:
        """Save a captured frame as an image."""

        if frame is None:
            self.logger.error("Cannot save empty frame.")
            return False

        try:
            result = cv2.imwrite(filename, frame)

            if result:
                self.logger.info("Frame saved: %s", filename)
                return True

            self.logger.error("Failed to save frame: %s", filename)
            return False

        except Exception as error:
            self.logger.exception(
                "Error while saving frame: %s",
                error
            )
            return False

    def __enter__(self):
        """Support context manager usage."""

        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Release camera automatically."""

        self.stop()