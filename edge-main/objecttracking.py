from ultralytics import YOLO
import cv2

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Track objects
    results = model.track(frame, persist=True)

    # Draw tracking boxes and IDs
    annotated_frame = results[0].plot()

    cv2.imshow("VisionEdge - Object Tracking", annotated_frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()