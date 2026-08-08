import cv2
import logging

from video_decoder import CameraManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def main():

    camera = CameraManager(
        camera_id=0,
        width=1280,
        height=720
    )

    print("=" * 60)
    print("VisionEdge Camera Manager Test")
    print("=" * 60)

    if not camera.start():
        print("[ERROR] Camera could not be started.")
        return

    print("[✓] Camera started successfully")

    resolution = camera.get_resolution()

    if resolution:
        print(
            f"[✓] Resolution: "
            f"{resolution[0]}x{resolution[1]}"
        )

    print("[✓] Camera window opened")
    print("[✓] Press Q inside the camera window to stop")
    print("[✓] Press ESC inside the camera window to stop")

    try:

        while True:

            frame = camera.read_frame()

            if frame is None:
                print("[WARNING] Frame capture failed. Retrying...")
                
                # Keep OpenCV's event processing alive
                key = cv2.waitKey(10) & 0xFF

                if key == ord("q") or key == ord("Q") or key == 27:
                    break

                continue

            cv2.imshow(
                "VisionEdge - Camera Test",
                frame
            )

            # IMPORTANT:
            # The camera window must have focus.
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == ord("Q") or key == 27:
                print("[INFO] Stop key pressed.")
                break

    except KeyboardInterrupt:

        print("\n[INFO] Camera interrupted by user.")

    finally:

        camera.stop()
        cv2.destroyAllWindows()

        print("[✓] Camera released")
        print("[✓] Camera test completed")


if __name__ == "__main__":
    main()