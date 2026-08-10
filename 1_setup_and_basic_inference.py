# =============================================================
# FILE 1 of 4: Setup & Basic Inference
# Source: Cells 0, 5, 1 (original notebook order)
# =============================================================

# ---------------------------------------------------------------
# CELL 1 (orig. Cell 0) — Install Ultralytics
# ---------------------------------------------------------------
!pip install ultralytics


# ---------------------------------------------------------------
# CELL 2 (orig. Cell 5) — Install PyAV (video decoding library)
# ---------------------------------------------------------------
!pip install av


# ---------------------------------------------------------------
# CELL 3 (orig. Cell 1) — Run YOLO Object Detection on a Sample Image
# ---------------------------------------------------------------
from ultralytics import YOLO

# Load a lightweight pre-trained YOLO model
model = YOLO('yolo11n.pt')

# Run object detection on a sample image
results = model('https://ultralytics.com/images/bus.jpg')

# Save the output image with boxes drawn around detected objects
results[0].save('output.jpg')
