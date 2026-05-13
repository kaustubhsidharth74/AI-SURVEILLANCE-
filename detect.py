import cv2
from ultralytics import YOLO
import os
from datetime import datetime
import time
from playsound import playsound
import threading

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Cannot access webcam")
    exit()

# Create screenshots folder
os.makedirs("screenshots", exist_ok=True)

# Time control
last_saved_time = 0
save_interval = 5  # seconds

# Play alarm in separate thread
def play_alarm():
    playsound("alarm.mp3")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Cannot receive frame")
        break

    # Run YOLO
    results = model(frame)

    person_detected = False

    # Process detections
    for result in results:
        boxes = result.boxes

        for box in boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # Detect only person with confidence > 50%
            if class_id == 0 and confidence > 0.5:
                person_detected = True

    # Draw detections
    annotated_frame = results[0].plot()

    current_time = time.time()

    # If person detected
    if person_detected:

        # Display alert text
        cv2.putText(
            annotated_frame,
            "INTRUDER DETECTED!",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        # Save only every 5 seconds
        if current_time - last_saved_time > save_interval:

            # Save screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/intruder_{timestamp}.jpg"

            cv2.imwrite(filename, annotated_frame)

            print(f"Screenshot saved: {filename}")

            # Play alarm
            threading.Thread(target=play_alarm).start()

            last_saved_time = current_time

    # Show output
    cv2.imshow("AI Smart Surveillance", annotated_frame)

    # Exit on q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()