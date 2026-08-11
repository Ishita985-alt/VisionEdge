import logging
from pathlib import Path

import numpy as np

from video_recorder import VideoRecorder


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def test_video_recorder():
    print("\n# VisionEdge Video Recorder Test\n")

    recorder = VideoRecorder(
        output_dir="../output/recordings",
        fps=20.0,
        codec="mp4v",
    )

    print("[✓] VideoRecorder initialized")

    # Create a sample 1280x720 frame
    test_frame = np.zeros(
        (720, 1280, 3),
        dtype=np.uint8,
    )

    print("[✓] Test frame created")
    print(
        f"[✓] Frame resolution: "
        f"{test_frame.shape[1]}x{test_frame.shape[0]}"
    )

    # Start recording
    started = recorder.start(
        test_frame,
        filename="test_recording.mp4",
    )

    if not started:
        print("[✗] Failed to start recording")
        return

    print("[✓] Recording started")

    # Write multiple frames
    frames_written = 0

    for _ in range(30):
        if recorder.write_frame(test_frame):
            frames_written += 1

    print(f"[✓] Frames written: {frames_written}")

    # Stop recording
    stopped = recorder.stop()

    if not stopped:
        print("[✗] Failed to stop recording")
        return

    print("[✓] Recording stopped")

    # Check output file
    output_path = recorder.get_output_path()

    if output_path is not None and Path(output_path).exists():
        file_size = Path(output_path).stat().st_size

        print(f"[✓] Recording file created: {output_path}")
        print(f"[✓] Recording file size: {file_size} bytes")
    else:
        print("[✗] Recording file was not created")
        return

    recorder.release()

    print("[✓] Recorder resources released")
    print("[✓] Day 5 Video Recorder test completed successfully")


def test_invalid_frame():
    print("\n# Invalid Frame Test\n")

    recorder = VideoRecorder(
        output_dir="../output/recordings",
        fps=20.0,
        codec="mp4v",
    )

    result = recorder.start(
        None,
        filename="invalid_recording.mp4",
    )

    if result is False:
        print("[✓] Invalid frame handled correctly")
    else:
        print("[✗] Invalid frame was not handled correctly")

    recorder.release()


if __name__ == "__main__":
    test_video_recorder()
    test_invalid_frame()