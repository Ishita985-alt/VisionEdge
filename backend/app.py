import atexit
import logging
from datetime import datetime
from pathlib import Path

from flask import Flask, Response, jsonify
from flask_cors import CORS

from camera_manager import CameraManager

from config import (
    OUTPUT_DIR,
    LOG_DIR,
    SNAPSHOT_DIR,
    RECORDING_DIR,
    DATABASE_DIR,
    MODELS_DIR,
    STREAMS_DIR,
    IMAGES_DIR,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    ENABLE_DATABASE,
)


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger("VisionEdge")


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        },
        r"/start_camera": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        },
        r"/stop_camera": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        },
        r"/capture_snapshot": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        },
        r"/video_feed": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        },
        r"/health": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        },
    },
)


# =========================================================
# VISIONEDGE BACKEND
# =========================================================

class VisionEdgeBackend:

    def __init__(self):

        self.project_name = (
            "VisionEdge AI Surveillance Studio"
        )

        self.version = "1.0.0"

        self.create_directories()

        logger.info(
            "Initializing Camera Manager..."
        )

        try:
            self.camera_manager = CameraManager()

            logger.info(
                "Camera Manager initialized successfully."
            )

        except Exception:

            logger.exception(
                "Camera Manager initialization failed."
            )

            raise


    # =====================================================
    # CREATE DIRECTORIES
    # =====================================================

    def create_directories(self):

        folders = [
            OUTPUT_DIR,
            LOG_DIR,
            SNAPSHOT_DIR,
            RECORDING_DIR,
            DATABASE_DIR,
            MODELS_DIR,
            STREAMS_DIR,
            IMAGES_DIR,
        ]

        for folder in folders:

            Path(folder).mkdir(
                parents=True,
                exist_ok=True,
            )

        logger.info(
            "Backend directories initialized."
        )


    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    def get_status(self):

        try:

            status = self.camera_manager.get_status()

        except Exception as error:

            logger.exception(
                "Unable to get camera status."
            )

            status = {
                "camera": "ERROR",
                "error": str(error),
            }

        status["application"] = (
            self.project_name
        )

        status["version"] = (
            self.version
        )

        status["resolution"] = (
            f"{FRAME_WIDTH} × {FRAME_HEIGHT}"
        )

        status["database"] = (
            "CONNECTED"
            if ENABLE_DATABASE
            else "DISABLED"
        )

        return status


# =========================================================
# CREATE BACKEND
# =========================================================

backend = VisionEdgeBackend()


# =========================================================
# ROOT / API INFORMATION
# =========================================================

@app.route("/")
def root():

    return jsonify({
        "application": backend.project_name,
        "version": backend.version,
        "status": "online",
        "frontend": "React / Vite",
        "frontend_url": "http://localhost:5173",
        "backend_url": "http://127.0.0.1:5000",
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    try:

        camera_status = (
            backend.camera_manager.camera_status
        )

    except Exception:

        camera_status = "ERROR"

    return jsonify({
        "status": "online",
        "application": backend.project_name,
        "version": backend.version,
        "camera": camera_status,
    })


# =========================================================
# SYSTEM STATUS API
# =========================================================

@app.route("/api/status")
def api_status():

    try:

        return jsonify(
            backend.get_status()
        )

    except Exception as error:

        logger.exception(
            "Failed to retrieve system status."
        )

        return jsonify({
            "success": False,
            "message": str(error),
        }), 500


# =========================================================
# START CAMERA
# =========================================================

@app.route(
    "/start_camera",
    methods=["POST"],
)
def start_camera():

    try:

        success = (
            backend.camera_manager.start()
        )

        if success:

            return jsonify({
                "success": True,
                "message": (
                    "Camera started successfully."
                ),
            })

        return jsonify({
            "success": False,
            "message": (
                "Camera could not be opened."
            ),
        }), 500

    except Exception as error:

        logger.exception(
            "Failed to start camera."
        )

        return jsonify({
            "success": False,
            "message": str(error),
        }), 500


# =========================================================
# STOP CAMERA
# =========================================================

@app.route(
    "/stop_camera",
    methods=["POST"],
)
def stop_camera():

    try:

        backend.camera_manager.stop()

        return jsonify({
            "success": True,
            "message": (
                "Camera stopped successfully."
            ),
        })

    except Exception as error:

        logger.exception(
            "Failed to stop camera."
        )

        return jsonify({
            "success": False,
            "message": str(error),
        }), 500


# =========================================================
# LIVE VIDEO STREAM
# =========================================================

@app.route("/video_feed")
def video_feed():

    try:

        if not backend.camera_manager.running:

            return (
                "Camera is offline.",
                503,
            )

        return Response(
            backend.camera_manager.generate_frames(),
            mimetype=(
                "multipart/x-mixed-replace; "
                "boundary=frame"
            ),
        )

    except Exception as error:

        logger.exception(
            "Video feed failed."
        )

        return (
            str(error),
            500,
        )


# =========================================================
# EVENTS API
# =========================================================

@app.route("/api/events")
def api_events():

    try:

        database = (
            backend.camera_manager.database
        )

        if database is None:

            return jsonify([])

        events = database.get_events(
            limit=100
        )

        return jsonify(events)

    except Exception as error:

        logger.exception(
            "Failed to retrieve events."
        )

        return jsonify({
            "success": False,
            "message": str(error),
        }), 500


# =========================================================
# CAPTURE SNAPSHOT
# =========================================================

@app.route(
    "/capture_snapshot",
    methods=["POST"],
)
def capture_snapshot():

    try:

        snapshot_directory = Path(
            SNAPSHOT_DIR
        )

        snapshot_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"snapshot_{timestamp}.jpg"
        )

        snapshot_path = (
            snapshot_directory / filename
        )

        success = (
            backend.camera_manager.capture_snapshot(
                snapshot_path
            )
        )

        if success:

            return jsonify({
                "success": True,
                "filename": filename,
                "message": (
                    "Snapshot captured successfully."
                ),
            })

        return jsonify({
            "success": False,
            "message": (
                "No camera frame available."
            ),
        }), 400

    except Exception as error:

        logger.exception(
            "Snapshot capture failed."
        )

        return jsonify({
            "success": False,
            "message": str(error),
        }), 500


# =========================================================
# CLEANUP
# =========================================================

def cleanup():

    logger.info(
        "Cleaning up VisionEdge..."
    )

    try:

        backend.camera_manager.stop()

    except Exception:

        logger.exception(
            "Error while stopping camera."
        )


atexit.register(cleanup)


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    logger.info("=" * 60)

    logger.info(
        "VisionEdge AI Surveillance Studio"
    )

    logger.info(
        "Version: %s",
        backend.version,
    )

    logger.info(
        "React Frontend: http://localhost:5173"
    )

    logger.info(
        "Flask Backend: http://127.0.0.1:5000"
    )

    logger.info(
        "Starting Flask server..."
    )

    logger.info("=" * 60)

    try:

        app.run(
            host="127.0.0.1",
            port=5000,
            debug=False,
            threaded=True,
        )

    except KeyboardInterrupt:

        logger.info(
            "VisionEdge stopped by user."
        )

    finally:

        cleanup()