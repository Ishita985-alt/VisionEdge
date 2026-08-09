import logging
from typing import Optional

import cv2
import numpy as np


logger = logging.getLogger("VisionEdge.FrameProcessor")


class FrameProcessor:
    """
    Handles validation and basic preprocessing of camera frames.

    Responsibilities:
    - Validate incoming frames
    - Resize frames when required
    - Return processed frames
    """

    def __init__(
        self,
        target_width: Optional[int] = None,
        target_height: Optional[int] = None,
    ):
        self.target_width = target_width
        self.target_height = target_height

        logger.info(
            "FrameProcessor initialized: target_size=%sx%s",
            self.target_width,
            self.target_height,
        )

    def validate_frame(self, frame: np.ndarray) -> bool:
        """Validate whether the input frame is usable."""

        if frame is None:
            logger.warning("Received empty frame.")
            return False

        if not isinstance(frame, np.ndarray):
            logger.warning("Invalid frame type: %s", type(frame))
            return False

        if frame.size == 0:
            logger.warning("Received empty NumPy frame.")
            return False

        if len(frame.shape) != 3:
            logger.warning(
                "Invalid frame dimensions: %s",
                frame.shape,
            )
            return False

        return True

    def resize_frame(self, frame: np.ndarray) -> np.ndarray:
        """Resize frame if target dimensions are configured."""

        if self.target_width is None or self.target_height is None:
            return frame

        return cv2.resize(
            frame,
            (self.target_width, self.target_height),
            interpolation=cv2.INTER_LINEAR,
        )

    def process(self, frame: np.ndarray) -> Optional[np.ndarray]:
        """
        Validate and preprocess a single frame.

        Returns:
            Processed frame if successful.
            None if the frame is invalid.
        """

        if not self.validate_frame(frame):
            return None

        try:
            processed_frame = self.resize_frame(frame)

            logger.debug(
                "Frame processed successfully: shape=%s",
                processed_frame.shape,
            )

            return processed_frame

        except Exception:
            logger.exception("Error while processing frame.")
            return None