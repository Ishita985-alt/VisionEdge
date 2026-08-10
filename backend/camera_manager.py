

import logging
import time
from threading import Lock

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
)

from database_manager import DatabaseManager


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
    - Flask video streaming
    - Snapshot capture
    """

    def __init__(self):

        # -------------------------------------------------
        # Camera
        # -------------------------------------------------

        self.camera = None
        self.running = False
        self.camera_status = "OFFLINE"

        # -------------------------------------------------
        # Thread safety
        # -------------------------------------------------

        self.lock = Lock()

        # -------------------------------------------------
        # Frame information
        # -------------------------------------------------

        self.latest_frame = None

        # -------------------------------------------------
        # Performance information
        # -------------------------------------------------

        self.current_fps = 0.0
        self.inference_time = 0.0

        # -------------------------------------------------
        # Detection information
        # -------------------------------------------------

        self.total_detections = 0

        # -------------------------------------------------
        # FPS timer
        # -------------------------------------------------

        self._previous_frame_time = None

        # -------------------------------------------------
        # Load YOLO
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Database
        # -------------------------------------------------

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

        self.running = True
        self.camera_status = "ONLINE"


        logger.info(
            "Camera started successfully."
        )


        return True


    # =====================================================
    # STOP CAMERA
    # =====================================================

    def stop(self):

        self.running = False


        if self.camera is not None:

            self.camera.release()

            self.camera = None


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
        # YOLO inference
        # -------------------------------------------------

        results = self.model(
            frame,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )


        inference_end = (
            time.perf_counter()
        )


        self.inference_time = (
            inference_end - start_time
        ) * 1000


        # -------------------------------------------------
        # Annotated frame
        # -------------------------------------------------

        annotated_frame = (
            results[0].plot()
        )


        # -------------------------------------------------
        # Detection information
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
        # Database event
        # -------------------------------------------------

        if (
            detection_count > 0
            and self.database is not None
        ):

            names = results[0].names

            detected_objects = []


            for box in detections:

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


            description = ", ".join(
                detected_objects
            )


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


        success, frame = (
            self.camera.read()
        )


        if not success:

            logger.error(
                "Could not read camera frame."
            )

            return None


        # -------------------------------------------------
        # FPS
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
        # AI processing
        # -------------------------------------------------

        annotated_frame = (
            self.process_frame(frame)
        )


        # -------------------------------------------------
        # FPS overlay
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
        # VisionEdge status
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
        # Store latest frame
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

                return False


            frame = (
                self.latest_frame.copy()
            )


        success = cv2.imwrite(
            str(path),
            frame
        )


        if success:

            logger.info(
                "Snapshot saved: %s",
                path
            )

        else:

            logger.error(
                "Failed to save snapshot: %s",
                path
            )


        return success


    # =====================================================
    # STATUS
    # =====================================================

    def get_status(self):

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
        }
