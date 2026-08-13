import cv2
import sqlite3
from ultralytics import YOLO
from datetime import datetime

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Create SQLite database
conn = sqlite3.connect("visionedge.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS detections(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_name TEXT,
    confidence REAL,
    date TEXT,
    time TEXT
)
""")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)

    annotated = results[0].plot()

    for box in results[0].boxes:

        cls = int(box.cls)
        name = model.names[cls]
        confidence = float(box.conf)

        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")

        cursor.execute(
            "INSERT INTO detections(object_name, confidence, date, time) VALUES (?, ?, ?, ?)",
            (name, confidence, date, time)
        )

    conn.commit()

    cv2.imshow("VisionEdge Database Logger", annotated)

    if cv2.waitKey(1) == 27:
        break

cap.release()
conn.close()
cv2.destroyAllWindows()

print("Detection data saved successfully!")
