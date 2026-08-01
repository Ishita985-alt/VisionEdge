import cv2
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")
result = model

# Open webcam
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Camera could not be opened.")
    exit()

# Get webcam video size
frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create output video file
output = cv2.VideoWriter(
    "output_detected.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    20,
    (frame_width, frame_height)
)

previous_time = time.time()

print("VisionEdge started.")
print("Detected video is being saved as output_detected.mp4")
print("Press Q to stop.")

while True:
    success, frame = camera.read()

    if not success:
        print("Error: Could not read camera frame.")
        break

    # Run YOLO object detection
    results = model(frame, verbose=False)

    # Draw detection boxes and labels
    annotated_frame = results[0].plot()

    # Calculate FPS
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    # Show FPS on the video
    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.1f}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Save the detected frame to the output video
    output.write(annotated_frame)

    # Show live video
    cv2.imshow("VisionEdge - Live Detection", annotated_frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release camera and save the video properly
camera.release()
output.release()
cv2.destroyAllWindows()

print("Video saved successfully as output_detected.mp4")