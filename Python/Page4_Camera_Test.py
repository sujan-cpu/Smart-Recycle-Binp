import cv2

CAMERA_INDEX = 0  # Change to 1 if your USB webcam is camera 1.
camera = cv2.VideoCapture(CAMERA_INDEX)

if not camera.isOpened():
    raise SystemExit("Camera not found. Try CAMERA_INDEX = 1.")

print("Camera test started. Press Q to quit.")
while True:
    ok, frame = camera.read()
    if not ok:
        print("Could not read a frame.")
        break
    cv2.imshow("Smart Recycling Bin - Camera Test", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
