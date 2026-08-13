import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Get frame size
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create output video file
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter("VisionEdge_Output.avi", fourcc, 20.0, (width, height))
print("Video Writer Open:", out.isOpened())

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Object detection
    results = model(frame)

    # Draw detection results
    annotated_frame = results[0].plot()

    # Save frame to video
    out.write(annotated_frame)

    # Display live video
    cv2.imshow("VisionEdge Recording", annotated_frame)

    # Press ESC to stop recording
    if cv2.waitKey(1) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("Video saved as VisionEdge_Output.mp4")