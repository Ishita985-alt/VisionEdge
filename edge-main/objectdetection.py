import cv2
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Run object detection
    results = model(frame)

    # Draw bounding boxes
    annotated_frame = results[0].plot()

    # Show output
    cv2.imshow("VisionEdge - Object Detection", annotated_frame)

    # Press ESC to exit
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()