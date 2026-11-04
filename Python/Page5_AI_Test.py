from pathlib import Path
import cv2
import numpy as np
from tensorflow.keras.models import load_model

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "Model" / "keras_model.h5"
LABELS_PATH = ROOT / "Model" / "labels.txt"
CAMERA_INDEX = 0

if not MODEL_PATH.exists() or not LABELS_PATH.exists():
    raise SystemExit("Put keras_model.h5 and labels.txt in the Model folder.")

model = load_model(str(MODEL_PATH), compile=False)
labels = [x.strip() for x in LABELS_PATH.read_text().splitlines() if x.strip()]

def clean_label(label):
    parts = label.strip().split(maxsplit=1)
    if len(parts) == 2 and parts[0].isdigit():
        return parts[1].strip().lower()
    return label.strip().lower()

camera = cv2.VideoCapture(CAMERA_INDEX)
if not camera.isOpened():
    raise SystemExit("Camera not found. Try CAMERA_INDEX = 1.")

print("AI test running. Press Q to quit.")
while True:
    ok, frame = camera.read()
    if not ok:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = cv2.resize(rgb, (224, 224)).astype(np.float32)
    image = (image / 127.5) - 1.0
    image = np.expand_dims(image, axis=0)

    scores = model.predict(image, verbose=0)[0]
    index = int(np.argmax(scores))
    label = clean_label(labels[index])
    confidence = float(scores[index])

    cv2.putText(frame, f"{label} - {confidence * 100:.1f}%",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Smart Recycling Bin - AI Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
