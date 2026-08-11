import logging
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


logger = logging.getLogger("VisionEdge.VideoRecorder")


class VideoRecorder:
    """
    Handles video recording from OpenCV frames.

    Responsibilities:
    - Create recording directory
    - Initialize video writer
    - Start recording
    - Write frames
    - Stop recording
    - Release resources
    - Handle recording errors
    """

    def __init__(
        self,
        output_dir: str = "output/recordings",
        fps: float = 20.0,
        codec: str = "mp4v",
    ):
        self.output_dir = Path(output_dir)
        self.fps = fps
        self.codec = codec

        self.writer: Optional[cv2.VideoWriter] = None
        self.output_path: Optional[Path] = None
        self.frame_size: Optional[tuple[int, int]] = None
        self._recording = False

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "VideoRecorder initialized: output_dir=%s, fps=%s, codec=%s",
            self.output_dir,
            self.fps,
            self.codec,
        )

    def start(
        self,
        frame: np.ndarray,
        filename: str = "visionedge_recording.mp4",
    ) -> bool:
        """
        Start video recording using the dimensions of the first frame.
        """

        if self._recording:
            logger.warning("Recording is already active.")
            return False

        if not self._validate_frame(frame):
            return False

        try:
            height, width = frame.shape[:2]

            self.frame_size = (width, height)
            self.output_path = self.output_dir / filename

            fourcc = cv2.VideoWriter_fourcc(*self.codec)

            self.writer = cv2.VideoWriter(
                str(self.output_path),
                fourcc,
                self.fps,
                self.frame_size,
            )

            if not self.writer.isOpened():
                logger.error(
                    "Failed to open video writer: %s",
                    self.output_path,
                )

                self.writer.release()
                self.writer = None
                return False

            self._recording = True

            logger.info(
                "Video recording started: %s",
                self.output_path,
            )

            return True

        except Exception:
            logger.exception("Error while starting video recording.")

            self.writer = None
            self._recording = False

            return False

    def write_frame(self, frame: np.ndarray) -> bool:
        """
        Write one frame to the active recording.
        """

        if not self._recording or self.writer is None:
            logger.warning(
                "Cannot write frame: recording is not active."
            )
            return False

        if not self._validate_frame(frame):
            return False

        try:
            if self.frame_size is None:
                logger.error("Frame size is not initialized.")
                return False

            width, height = self.frame_size

            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(
                    frame,
                    self.frame_size,
                    interpolation=cv2.INTER_LINEAR,
                )

            self.writer.write(frame)

            return True

        except Exception:
            logger.exception("Error while writing video frame.")
            return False

    def stop(self) -> bool:
        """
        Stop recording and release the video writer.
        """

        if not self._recording:
            logger.warning("Recording is not active.")
            return False

        try:
            if self.writer is not None:
                self.writer.release()

            self.writer = None
            self._recording = False

            logger.info(
                "Video recording stopped: %s",
                self.output_path,
            )

            return True

        except Exception:
            logger.exception("Error while stopping video recording.")

            self.writer = None
            self._recording = False

            return False

    def is_recording(self) -> bool:
        """
        Return whether recording is currently active.
        """

        return self._recording

    def get_output_path(self) -> Optional[Path]:
        """
        Return the current recording output path.
        """

        return self.output_path

    @staticmethod
    def _validate_frame(frame: np.ndarray) -> bool:
        """
        Validate an OpenCV frame.
        """

        if frame is None:
            logger.warning("Received empty frame.")
            return False

        if not isinstance(frame, np.ndarray):
            logger.warning(
                "Invalid frame type: %s",
                type(frame),
            )
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

    def release(self) -> None:
        """
        Safely release recording resources.
        """

        if self.writer is not None:
            self.writer.release()

        self.writer = None
        self._recording = False

        logger.info("VideoRecorder resources released.")