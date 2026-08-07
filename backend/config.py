"""
VisionEdge Backend Configuration
"""

from pathlib import Path

# -----------------------------
# Base Project Directory
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------
# Resource Directories
# -----------------------------
MODELS_DIR = BASE_DIR / "models"
STREAMS_DIR = BASE_DIR / "streams"
IMAGES_DIR = BASE_DIR / "Images"

# -----------------------------
# Output Directories
# -----------------------------
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = OUTPUT_DIR / "logs"
SNAPSHOT_DIR = OUTPUT_DIR / "snapshots"
RECORDING_DIR = OUTPUT_DIR / "recordings"
DATABASE_DIR = OUTPUT_DIR / "database"

# -----------------------------
# Camera Settings
# -----------------------------
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 30

# -----------------------------
# AI Settings
# -----------------------------
MODEL_NAME = "yolov10.pt"
CONFIDENCE_THRESHOLD = 0.50

# -----------------------------
# Feature Flags
# -----------------------------
ENABLE_RECORDING = True
ENABLE_SNAPSHOTS = True
ENABLE_DATABASE = True

# -----------------------------
# Database
# -----------------------------
DATABASE_NAME = "visionedge.db"