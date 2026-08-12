# =============================================================
# FILE 3 of 4: Benchmarking & Profiling
# Source: Cells 7, 8, 9, 10, 11 (original notebook order)
# =============================================================

# ---------------------------------------------------------------
# CELL 1 (orig. Cell 7) — Frame-by-Frame Inference Latency Benchmark (PyAV)
# ---------------------------------------------------------------
import av
import time
from ultralytics import YOLO

# Step 1: Load your YOLO model
model = YOLO('yolo11n.pt')

# Step 2: Open the sample video stream using PyAV
video_url = 'https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/person-bicycle-car-detection.mp4'
container = av.open(video_url)

total_latency = 0
frame_count = 0

print("Starting Inference Loop...\n")

# Step 3: Run the loop across video frames
for frame in container.decode(video=0):
    # Convert PyAV frame to standard image format
    img = frame.to_ndarray(format="bgr24")

    # Record start time
    start_time = time.time()

    # Run AI inference on the frame
    results = model(img, verbose=False)

    # Record end time & calculate latency in milliseconds (ms)
    frame_latency = (time.time() - start_time) * 1000

    total_latency += frame_latency
    frame_count += 1

    # Stop after testing 30 frames
    if frame_count >= 30:
        break

# Step 4: Calculate Average Latency
avg_latency = total_latency / frame_count
fps = 1000 / avg_latency

print("--- BENCHMARK RESULTS ---")
print(f"Processed Frames: {frame_count}")
print(f"Average Latency: {avg_latency:.2f} ms per frame")
print(f"Estimated Speed:  {fps:.1f} Frames Per Second (FPS)")


# ---------------------------------------------------------------
# CELL 2 (orig. Cell 8) — PyTorch vs TensorRT Speed Comparison
# ---------------------------------------------------------------
import time
from ultralytics import YOLO

# 1. Measure Native PyTorch Speed
pytorch_model = YOLO('yolo11n.pt')
t0 = time.time()
for _ in range(50):
    results_pt = pytorch_model('https://ultralytics.com/images/bus.jpg', verbose=False)
pytorch_time = (time.time() - t0) / 50
pytorch_fps = 1.0 / pytorch_time

# 2. Measure TensorRT Engine Speed
trt_model = YOLO('yolo11n.engine')
t0 = time.time()
for _ in range(50):
    results_trt = trt_model('https://ultralytics.com/images/bus.jpg', verbose=False)
trt_time = (time.time() - t0) / 50
trt_fps = 1.0 / trt_time

# 3. Calculate Speedup Ratio
speedup = trt_fps / pytorch_fps

print("=== PERFORMANCE AUDIT RESULTS ===")
print(f"PyTorch Native FPS : {pytorch_fps:.2f} FPS")
print(f"TensorRT Engine FPS: {trt_fps:.2f} FPS")
print(f"Speedup Achieved   : {speedup:.2f}x faster")

if speedup >= 3.0:
    print("SUCCESS: Meets the 3x performance requirement!")
else:
    print("WARNING: Speedup is below 3x. Further FP16/INT8 precision tuning required.")


# ---------------------------------------------------------------
# CELL 3 (orig. Cell 9) — VRAM / Memory Leak Profiling
# ---------------------------------------------------------------
import torch
import time
from ultralytics import YOLO

model = YOLO('yolo11n.pt')

print("=== MEMORY PROFILING (VRAM) ===")
initial_memory = torch.cuda.memory_allocated() / (1024 ** 2)
print(f"Initial Allocated VRAM: {initial_memory:.2f} MB")

# Simulate continuous streaming
for frame_idx in range(1, 101):
    results = model('https://ultralytics.com/images/bus.jpg', verbose=False)

    if frame_idx % 25 == 0:
        current_memory = torch.cuda.memory_allocated() / (1024 ** 2)
        print(f"Frame {frame_idx:3d} | Current VRAM: {current_memory:.2f} MB")

final_memory = torch.cuda.memory_allocated() / (1024 ** 2)
memory_leak = final_memory - initial_memory

print(f"\nMemory Leak Check: {memory_leak:.2f} MB difference across 100 frames.")
if abs(memory_leak) < 5.0:
    print("SUCCESS: Memory profile is stable. No VRAM leaks detected!")
else:
    print("WARNING: Possible memory leak detected!")


# ---------------------------------------------------------------
# CELL 4 (orig. Cell 10) — Export Model to TensorRT with FP16 Half-Precision
# ---------------------------------------------------------------
from ultralytics import YOLO

# 1. Load the original PyTorch model
model = YOLO('yolo11n.pt')

# 2. Export to TensorRT with half-precision (FP16) enabled
model.export(format='engine', half=True, workspace=4)

# NOTE: You requested live camera output. This cell is for model export.
# Implementing live camera functionality in Colab typically requires a separate
# code cell that utilizes browser-based webcam access (often with JavaScript)
# and then passes those frames to a model for processing.
# This functionality would best be placed in a new, dedicated cell.


# ---------------------------------------------------------------
# CELL 5 (orig. Cell 11) — Updated PyTorch vs FP16 TensorRT Speedup Audit
# ---------------------------------------------------------------
import time
from ultralytics import YOLO

# 1. Benchmark PyTorch
pt_model = YOLO('yolo11n.pt')
t0 = time.time()
for _ in range(50):
    pt_model('https://ultralytics.com/images/bus.jpg', verbose=False)
pt_time = (time.time() - t0) / 50
pt_fps = 1.0 / pt_time

# 2. Benchmark FP16 TensorRT Engine
trt_model = YOLO('yolo11n.engine')
t0 = time.time()
for _ in range(50):
    trt_model('https://ultralytics.com/images/bus.jpg', verbose=False)
trt_time = (time.time() - t0) / 50
trt_fps = 1.0 / trt_time

# 3. Calculate Speedup Ratio
speedup = trt_fps / pt_fps

print("\n=== UPDATED PERFORMANCE AUDIT ===")
print(f"PyTorch Native FPS : {pt_fps:.2f} FPS")
print(f"TensorRT FP16 FPS  : {trt_fps:.2f} FPS")
print(f"Speedup Achieved   : {speedup:.2f}x faster")

if speedup >= 3.0:
    print("SUCCESS: Performance audit passed! TensorRT is >3x faster.")
else:
    print(f"Current speedup: {speedup:.2f}x. Check GPU resource allocation in Colab.")
