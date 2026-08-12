import logging
import time
from threading import Lock
from pathlib import Path

import cv2
from ultralytics import YOLO

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FPS,
    MODEL_NAME,
    CONFIDENCE_THRESHOLD,
    ENABLE_DATABASE,
    RECORDING_DIR,
)

from database_manager import DatabaseManager
from recording.video_recorder import VideoRecorder


logger = logging.getLogger(
    "VisionEdge.CameraManager"
)


class CameraManager:
    """
    Handles:

    - Camera initialization
    - Live frame capture
    - YOLO inference
    - Detection annotation
    - FPS calculation
    - Database event creation
    - Video recording
    - Flask video streaming
    - Snapshot capture
    - Resource cleanup
    """

    def __init__(self):

        # =================================================
        # CAMERA
        # =================================================

        self.camera = None
        self.running = False
        self.camera_status = "OFFLINE"

        # =================================================
        # THREAD SAFETY
        # =================================================

        self.lock = Lock()

        # =================================================
        # FRAME INFORMATION
        # =================================================

        self.latest_frame = None

        # =================================================
        # PERFORMANCE INFORMATION
        # =================================================

        self.current_fps = 0.0
        self.inference_time = 0.0

        # =================================================
        # DETECTION INFORMATION
        # =================================================

        self.total_detections = 0

        # =================================================
        # FPS TIMER
        # =================================================

        self._previous_frame_time = None

        # =================================================
        # LOAD YOLO MODEL
        # =================================================

        logger.info(
            "Loading YOLO model: %s",
            MODEL_NAME
        )

        try:

            self.model = YOLO(
                MODEL_NAME
            )

            logger.info(
                "YOLO model loaded successfully."
            )

        except Exception:

            logger.exception(
                "Failed to load YOLO model."
            )

            raise

        # =================================================
        # VIDEO RECORDER
        # =================================================

        self.video_recorder = VideoRecorder(
            output_dir=str(RECORDING_DIR),
            fps=FPS,
            codec="mp4v",
        )

        logger.info(
            "Video Recorder initialized."
        )

        # =================================================
        # DATABASE
        # =================================================

        self.database = None

        if ENABLE_DATABASE:

            self.database = DatabaseManager()

            self.database.initialize_database()

            logger.info(
                "Database integration enabled."
            )

    # =====================================================
    # START CAMERA
    # =====================================================

    def start(self):

        if self.running:

            logger.warning(
                "Camera is already running."
            )

            return True

        logger.info(
            "Opening camera index %s",
            CAMERA_INDEX
        )

        try:

            self.camera = cv2.VideoCapture(
                CAMERA_INDEX
            )

            if not self.camera.isOpened():

                logger.error(
                    "Camera could not be opened."
                )

                self.camera = None
                self.running = False
                self.camera_status = "OFFLINE"

                return False

            # -------------------------------------------------
            # Camera resolution
            # -------------------------------------------------

            self.camera.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                FRAME_WIDTH
            )

            self.camera.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                FRAME_HEIGHT
            )

            self.camera.set(
                cv2.CAP_PROP_FPS,
                FPS
            )

            # -------------------------------------------------
            # Reset runtime values
            # -------------------------------------------------

            self._previous_frame_time = (
                time.perf_counter()
            )

            self.current_fps = 0.0
            self.inference_time = 0.0
            self.total_detections = 0
            self.latest_frame = None

            self.running = True
            self.camera_status = "ONLINE"
            # -------------------------------------------------
            # Start Video Recording
            # -------------------------------------------------

            success, frame = self.camera.read()

            if success:

                recording_started = self.video_recorder.start(
                    frame,
                    filename="visionedge_recording.mp4",
                )

                if recording_started:
                    logger.info(
                        "Video recording started successfully."
                    )
                else:
                    logger.warning(
                        "Video recording could not be started."
                    )

            else:

                logger.warning(
                    "Could not capture initial frame for recording."
                )

            logger.info(
                "Camera started successfully."
            )

            return True

        except Exception:

            logger.exception(
                "Camera initialization failed."
            )

            if self.camera is not None:

                self.camera.release()

                self.camera = None

            self.running = False
            self.camera_status = "OFFLINE"

            return False

    # =====================================================
    # STOP CAMERA
    # =====================================================

    def stop(self):

        self.running = False

        # -------------------------------------------------
        # Stop Video Recorder
        # -------------------------------------------------

        try:

            if self.video_recorder.is_recording():

                self.video_recorder.stop()

                logger.info(
                    "Video recording stopped with camera."
                )

        except Exception:

            logger.exception(
                "Failed to stop video recorder."
            )

        # -------------------------------------------------
        # Release Camera
        # -------------------------------------------------

        if self.camera is not None:

            self.camera.release()

            self.camera = None

        # -------------------------------------------------
        # Stop Video Recording
        # -------------------------------------------------

        if self.video_recorder.is_recording():

            self.video_recorder.stop()

            logger.info(
                "Video recording stopped with camera."
            )
        self.camera_status = "OFFLINE"

        logger.info(
            "Camera stopped."
        )

    # =====================================================
    # PROCESS FRAME
    # =====================================================

    def process_frame(self, frame):

        start_time = (
            time.perf_counter()
        )

        # -------------------------------------------------
        # YOLO INFERENCE
        # -------------------------------------------------

        try:

            results = self.model(
                frame,
                conf=CONFIDENCE_THRESHOLD,
                verbose=False
            )

        except Exception:

            logger.exception(
                "YOLO inference failed."
            )

            return frame

        inference_end = (
            time.perf_counter()
        )

        self.inference_time = (
            inference_end - start_time
        ) * 1000

        # -------------------------------------------------
        # ANNOTATED FRAME
        # -------------------------------------------------

        try:

            annotated_frame = (
                results[0].plot()
            )

        except Exception:

            logger.exception(
                "Failed to annotate frame."
            )

            return frame

        # -------------------------------------------------
        # DETECTION INFORMATION
        # -------------------------------------------------

        detections = results[0].boxes

        detection_count = 0

        if detections is not None:

            detection_count = len(
                detections
            )

        self.total_detections += (
            detection_count
        )

        # -------------------------------------------------
        # DATABASE EVENT
        # -------------------------------------------------

        if (
            detection_count > 0
            and self.database is not None
        ):

            names = results[0].names

            detected_objects = []

            for box in detections:

                try:

                    class_id = int(
                        box.cls[0]
                    )

                    confidence = float(
                        box.conf[0]
                    )

                    class_name = names[
                        class_id
                    ]

                    detected_objects.append(
                        f"{class_name} "
                        f"({confidence:.2f})"
                    )

                except Exception:

                    logger.exception(
                        "Failed to process detection."
                    )

            description = ", ".join(
                detected_objects
            )

            if description:

                try:

                    self.database.add_event(
                        camera_id=(
                            f"camera_{CAMERA_INDEX}"
                        ),
                        event_type=(
                            "object_detected"
                        ),
                        description=description,
                        severity="INFO"
                    )

                except Exception:

                    logger.exception(
                        "Failed to save detection event."
                    )

        return annotated_frame

    # =====================================================
    # READ FRAME
    # =====================================================

    def read_frame(self):

        if not self.running:

            return None

        if self.camera is None:

            return None

        # -------------------------------------------------
        # CAPTURE CAMERA FRAME
        # -------------------------------------------------

        success, frame = (
            self.camera.read()
        )

        if not success:

            logger.error(
                "Could not read camera frame."
            )

            return None

        # -------------------------------------------------
        # FPS CALCULATION
        # -------------------------------------------------

        current_time = (
            time.perf_counter()
        )

        if (
            self._previous_frame_time
            is not None
        ):

            elapsed = (
                current_time
                - self._previous_frame_time
            )

            if elapsed > 0:

                self.current_fps = (
                    1 / elapsed
                )

        self._previous_frame_time = (
            current_time
        )

        # -------------------------------------------------
        # AI PROCESSING
        # -------------------------------------------------

        annotated_frame = (
            self.process_frame(frame)
        )
        # -------------------------------------------------
        # Video Recording
        # -------------------------------------------------

        if self.video_recorder.is_recording():

            self.video_recorder.write_frame(
                annotated_frame
            )
        # -------------------------------------------------
        # FPS OVERLAY
        # -------------------------------------------------

        cv2.putText(
            annotated_frame,
            f"FPS: {self.current_fps:.1f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # -------------------------------------------------
        # VISIONEDGE STATUS
        # -------------------------------------------------

        cv2.putText(
            annotated_frame,
            "VisionEdge | LIVE",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # -------------------------------------------------
        # VIDEO RECORDING
        # -------------------------------------------------

        try:

            # Start recorder automatically
            # when the first valid frame arrives.

            if not self.video_recorder.is_recording():

                started = self.video_recorder.start(
                    annotated_frame,
                    filename="visionedge_recording.mp4",
                )

                if started:

                    logger.info(
                        "Video recording started."
                    )

            # Write current processed frame

            if self.video_recorder.is_recording():

                self.video_recorder.write_frame(
                    annotated_frame
                )

        except Exception:

            logger.exception(
                "Video recording failed."
            )

        # -------------------------------------------------
        # STORE LATEST FRAME
        # -------------------------------------------------

        with self.lock:

            self.latest_frame = (
                annotated_frame.copy()
            )

        return annotated_frame

    # =====================================================
    # FLASK VIDEO STREAM
    # =====================================================

    def generate_frames(self):

        while self.running:

            frame = self.read_frame()

            if frame is None:

                time.sleep(0.05)

                continue

            success, buffer = (
                cv2.imencode(
                    ".jpg",
                    frame
                )
            )

            if not success:

                logger.warning(
                    "Failed to encode frame."
                )

                continue

            frame_bytes = (
                buffer.tobytes()
            )

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes
                + b"\r\n"
            )

    # =====================================================
    # SNAPSHOT
    # =====================================================

    def capture_snapshot(self, path):

        with self.lock:

            if self.latest_frame is None:

                logger.warning(
                    "No frame available for snapshot."
                )

                return False

            frame = (
                self.latest_frame.copy()
            )

        try:

            snapshot_path = Path(
                path
            )

            snapshot_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            success = cv2.imwrite(
                str(snapshot_path),
                frame
            )

            if success:

                logger.info(
                    "Snapshot saved: %s",
                    snapshot_path
                )

            else:

                logger.error(
                    "Failed to save snapshot: %s",
                    snapshot_path
                )

            return success

        except Exception:

            logger.exception(
                "Snapshot capture failed."
            )

            return False

    # =====================================================
    # STATUS
    # =====================================================

    def get_status(self):

        recording_status = False

        try:

            recording_status = (
                self.video_recorder.is_recording()
            )

        except Exception:

            logger.exception(
                "Unable to retrieve recording status."
            )

        return {

            "camera_status": (
                self.camera_status
            ),

            "fps": round(
                self.current_fps,
                1
            ),

            "inference_time": round(
                self.inference_time,
                1
            ),

            "total_detections": (
                self.total_detections
            ),

            "recording": (
                recording_status
            ),
        }

    # =====================================================
    # RELEASE RESOURCES
    # =====================================================

    def release(self):

        logger.info(
            "Releasing CameraManager resources..."
        )

        try:

            self.stop()

        except Exception:

            logger.exception(
                "Error while stopping camera."
            )

        try:

            self.video_recorder.release()

        except Exception:

            logger.exception(
                "Error while releasing video recorder."
            )

        logger.info(
            "CameraManager resources released."
        )