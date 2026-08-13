import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Cannot access camera")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur image
    blur = cv2.GaussianBlur(frame, (15, 15), 0)

    # Detect edges
    edges = cv2.Canny(frame, 100, 200)

    # Display windows
    cv2.imshow("Original", frame)
    cv2.imshow("Grayscale", gray)
    cv2.imshow("Blur", blur)
    cv2.imshow("Edges", edges)

    # Press ESC to exit
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()