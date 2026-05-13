import cv2

# Open webcam
cap = cv2.VideoCapture(0)

# Check camera
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Read frame
    ret, frame = cap.read()

    # If frame not captured
    if not ret:
        print("Failed to grab frame")
        break

    # Show webcam
    cv2.imshow("AI Surveillance Camera", frame)

    # Press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()