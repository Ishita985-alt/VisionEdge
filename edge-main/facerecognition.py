import cv2
import face_recognition
import os
import pandas as pd
from datetime import datetime

known_encodings = []
known_names = []

path = "known_faces"

for file in os.listdir(path):
    if not file.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image = face_recognition.load_image_file(f"{path}/{file}")
    encoding = face_recognition.face_encodings(image)[0]
    known_encodings.append(encoding)
    known_names.append(os.path.splitext(file)[0])

cap = cv2.VideoCapture(0)

attendance = []

while True:
    success, frame = cap.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):

        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding
        )

        name = "Unknown"

        if True in matches:
            index = matches.index(True)
            name = known_names[index]

            if name not in attendance:
                attendance.append(name)

        top, right, bottom, left = face_location

        cv2.rectangle(frame,
                      (left, top),
                      (right, bottom),
                      (0,255,0),
                      2)

        cv2.putText(frame,
                    name,
                    (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2)

    cv2.imshow("VisionEdge Face Recognition", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()

df = pd.DataFrame({
    "Name": attendance,
    "Date": datetime.now().strftime("%Y-%m-%d"),
    "Time": datetime.now().strftime("%H:%M:%S")
})

df.to_csv("attendance.csv", index=False)

print("Attendance Saved")