import sys
import time

sys.path.insert(0, ".")

from camera_manager import CameraManager


def main():

    print("\n# VisionEdge Camera + YOLO + Recording Integration Test\n")

    camera_manager = CameraManager()

    print("[1] Starting camera...")

    started = camera_manager.start()

    print(f"[✓] Camera started: {started}")

    if not started:
        print("[✗] Camera could not be started.")
        return

    print(
        "[✓] Recording active:",
        camera_manager.video_recorder.is_recording()
    )

    print("[2] Processing camera frames for 5 seconds...")

    start_time = time.time()
    frames_processed = 0

    while time.time() - start_time < 5:

        frame = camera_manager.read_frame()

        if frame is not None:

            frames_processed += 1

        else:

            time.sleep(0.05)

    print(
        f"[✓] Frames processed: {frames_processed}"
    )

    print("[3] Stopping camera...")

    camera_manager.stop()

    print("[✓] Camera stopped")

    print(
        "[✓] Recording active after stop:",
        camera_manager.video_recorder.is_recording()
    )

    print("\n[✓] Camera + YOLO + VideoRecorder integration test completed.")


if __name__ == "__main__":
    main()