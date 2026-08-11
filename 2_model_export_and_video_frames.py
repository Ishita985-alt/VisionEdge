# =============================================================
# FILE 2 of 4: Model Export & Video Frame Extraction
# Source: Cells 2, 3, 4, 6 (original notebook order)
# =============================================================

# ---------------------------------------------------------------
# CELL 1 (orig. Cell 2) — Export Trained Model to ONNX Format
# ---------------------------------------------------------------
from ultralytics import YOLO

# 1. Load your trained model
model = YOLO('yolo11n.pt')

# 2. Export it to ONNX format
model.export(format='onnx')


# ---------------------------------------------------------------
# CELL 2 (orig. Cell 3) — Export Model to TensorRT Format
# ---------------------------------------------------------------
from ultralytics import YOLO

# Load the original model and compile directly into TensorRT format
model = YOLO('yolo11n.pt')
model.export(format='engine')


# ---------------------------------------------------------------
# CELL 3 (orig. Cell 4) — Extract and Count Raw Video Frames (PyAV)
# ---------------------------------------------------------------
import av

# 1. Open a sample video stream
container = av.open('https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4')

# 2. Extract and count raw frames from the video
frame_count = 0
for frame in container.decode(video=0):
    frame_count += 1
    # 'frame' is now a raw image ready for the AI to analyze!

print(f"Successfully extracted {frame_count} video frames!")


# ---------------------------------------------------------------
# CELL 4 (orig. Cell 6) — Measure Per-Frame Processing Time (Streaming)
# ---------------------------------------------------------------
import time
from ultralytics import YOLO

# Load the model
model = YOLO('yolo11n.pt')

# Process a video stream and measure time per frame
start_time = time.time()

# Run AI on a sample video feed
results = model('https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4', stream=True)

for i, r in enumerate(results):
    if i >= 30: # Test first 30 frames
        break

total_time = time.time() - start_time
average_latency = (total_time / 30) * 1000 # convert to milliseconds

print(f"Average processing time per frame: {average_latency:.2f} ms")
