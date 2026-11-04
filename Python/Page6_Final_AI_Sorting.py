from pathlib import Path
import time
import cv2
import numpy as np
import serial
from tensorflow.keras.models import load_model

# -------- EDIT THESE SETTINGS --------
ROOT = Path(__file__).resolve().parents[1]
SERIAL_PORT = "COM3"  # Windows: COM3; macOS: /dev/cu.usbmodemXXXX; Linux: /dev/ttyACM0
BAUD_RATE = 9600
CAMERA_INDEX = 0
CONFIDENCE_LIMIT = 0.85
REQUIRED_FRAMES = 5
# -------------------------------------

MODEL_PATH = ROOT / "Model" / "keras_model.h5"
LABELS_PATH = ROOT / "Model" / "labels.txt"

if not MODEL_PATH.exists() or not LABELS_PATH.exists():
    raise SystemExit("Model files missing: add keras_model.h5 and labels.txt to Model/.")

def clean_label(label):
    # Teachable Machine labels often look like '0 Plastic'.
    parts = label.strip().split(maxsplit=1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1].strip().lower()
    return label.strip().lower()

def category_from_label(label):
    label = clean_label(label)
    if "no object" in label or "background" in label or "empty" in label:
        return "NO OBJECT"
    if "plastic" in label:
        return "PLASTIC"
    if "paper" in label or "cardboard" in label:
        return "PAPER"
    if "metal" in label or "aluminum" in label or "aluminium" in label:
        return "METAL"
    return "UNKNOWN"

model = load_model(str(MODEL_PATH), compile=False)
labels = [x.strip() for x in LABELS_PATH.read_text().splitlines() if x.strip()]
if not labels:
    raise SystemExit("labels.txt is empty.")

print("Connecting to Arduino:", SERIAL_PORT)
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Arduino may reset when serial opens.

camera = cv2.VideoCapture(CAMERA_INDEX)
if not camera.isOpened():
    arduino.close()
    raise SystemExit("Camera not found. Try CAMERA_INDEX = 1.")

previous_category = None
stable_count = 0
armed = True

print("Running. Show one item at a time; remove it fully before the next item. Press Q to quit.")

try:
    while True:
        ok, frame = camera.read()
        if not ok:
            print("Camera frame could not be read.")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.resize(rgb, (224, 224)).astype(np.float32)
        image = (image / 127.5) - 1.0
        image = np.expand_dims(image, axis=0)

        scores = model.predict(image, verbose=0)[0]
        index = int(np.argmax(scores))
        confidence = float(scores[index])
        category = category_from_label(labels[index]) if index < len(labels) else "UNKNOWN"

        if confidence < CONFIDENCE_LIMIT:
            category = "UNKNOWN"

        if category == previous_category:
            stable_count += 1
        else:
            previous_category = category
            stable_count = 1

        if stable_count >= REQUIRED_FRAMES:
            if category == "NO OBJECT":
                armed = True
            elif category in ("PLASTIC", "PAPER", "METAL") and armed:
                command = {"PLASTIC": b"P", "PAPER": b"A", "METAL": b"M"}[category]
                print(f"{category} detected ({confidence * 100:.1f}%). Sorting...")
                arduino.write(command)
                arduino.flush()
                armed = False
            # UNKNOWN never activates the sorting mechanism.

        status = "READY" if armed else "REMOVE ITEM"
        display = f"{category} | {confidence * 100:.1f}% | {status}"
        cv2.putText(frame, display, (15, 35), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 255, 0), 2)
        cv2.imshow("Smart AI Recycling Bin", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    camera.release()
    cv2.destroyAllWindows()
    if arduino.is_open:
        arduino.close()
    print("Smart Recycling Bin stopped.")
