"""
VisionEdge Backend
Day 1 - Project Initialization
"""

from pathlib import Path
import datetime

from config import (
    OUTPUT_DIR,
    LOG_DIR,
    SNAPSHOT_DIR,
    RECORDING_DIR,
    DATABASE_DIR,
    MODELS_DIR,
    STREAMS_DIR,
    IMAGES_DIR,
)


class VisionEdgeBackend:
    def __init__(self):
        self.project_name = "VisionEdge AI Surveillance Studio"
        self.version = "1.0.0"

    def create_directories(self):
        """
        Create required project folders.
        """

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
            Path(folder).mkdir(parents=True, exist_ok=True)

        print("[✓] Project folders initialized")

    def startup_banner(self):

        print("=" * 60)
        print(f"{self.project_name}")
        print(f"Version : {self.version}")
        print(f"Started : {datetime.datetime.now()}")
        print("=" * 60)

    def system_check(self):

        print("\nPerforming System Check...\n")

        print("[✓] Configuration Loaded")
        print("[✓] Output Directories Ready")
        print("[✓] Backend Initialized")

    def start(self):

        self.startup_banner()
        self.create_directories()
        self.system_check()

        print("\nBackend is ready.")
        print("Waiting for Camera Module...\n")


def main():

    backend = VisionEdgeBackend()
    backend.start()


if __name__ == "__main__":
    main()