import logging

import numpy as np

from frame_processor import FrameProcessor


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def test_frame_processor():
    print("\n# VisionEdge Frame Processor Test\n")

    processor = FrameProcessor(
        target_width=640,
        target_height=640,
    )

    # Create a sample 1280x720 OpenCV frame.
    test_frame = np.zeros(
        (720, 1280, 3),
        dtype=np.uint8,
    )

    print("[✓] Test frame created")
    print(
        f"[✓] Original resolution: "
        f"{test_frame.shape[1]}x{test_frame.shape[0]}"
    )

    # Test frame validation.
    if processor.validate_frame(test_frame):
        print("[✓] Frame validation successful")
    else:
        print("[✗] Frame validation failed")
        return

    # Process the frame.
    processed_frame = processor.process(test_frame)

    if processed_frame is None:
        print("[✗] Frame processing failed")
        return

    print(
        f"[✓] Processed resolution: "
        f"{processed_frame.shape[1]}x{processed_frame.shape[0]}"
    )

    print("[✓] Frame processing completed")
    print("[✓] Day 3 Frame Processor test successful")


def test_invalid_frame():
    print("\n# Invalid Frame Test\n")

    processor = FrameProcessor(
        target_width=640,
        target_height=640,
    )

    invalid_frame = None

    result = processor.process(invalid_frame)

    if result is None:
        print("[✓] Invalid frame handled correctly")
    else:
        print("[✗] Invalid frame was not handled correctly")


if __name__ == "__main__":
    test_frame_processor()
    test_invalid_frame()