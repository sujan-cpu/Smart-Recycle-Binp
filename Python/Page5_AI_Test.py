
# ==========================================
# SMART RECYCLING BIN - AI CAMERA TEST
# ==========================================

import os

# Enable legacy Keras BEFORE importing TensorFlow
os.environ["TF_USE_LEGACY_KERAS"] = "1"

from pathlib import Path
import cv2
import numpy as np

from tensorflow.keras.layers import DepthwiseConv2D
from tensorflow.keras.models import load_model


# ==========================================
# 1. COMPATIBILITY FIX
# ==========================================

class CompatibleDepthwiseConv2D(DepthwiseConv2D):

    @classmethod
    def from_config(cls, config):
        config = dict(config)
        config.pop("groups", None)
        return cls(**config)


# ==========================================
# 2. PROJECT PATHS
# ==========================================

ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = ROOT / "Model" / "keras_model.h5"
LABELS_PATH = ROOT / "Model" / "labels.txt"

CAMERA_INDEX = 0

IMAGE_SIZE = (224, 224)


# ==========================================
# 3. CHECK MODEL FILES
# ==========================================

if not MODEL_PATH.exists():
    raise SystemExit(
        "ERROR: keras_model.h5 not found in Model folder!"
    )

if not LABELS_PATH.exists():
    raise SystemExit(
        "ERROR: labels.txt not found in Model folder!"
    )


# ==========================================
# 4. LOAD LABELS
# ==========================================

labels = [
    x.strip()
    for x in LABELS_PATH.read_text().splitlines()
    if x.strip()
]


def clean_label(label):

    parts = label.strip().split(maxsplit=1)

    if len(parts) == 2 and parts[0].isdigit():
        return parts[1].strip().lower()

    return label.strip().lower()


# ==========================================
# 5. LOAD AI MODEL
# ==========================================

print("----------------------------------")
print("SMART RECYCLING BIN")
print("----------------------------------")

print("Loading AI model...")

try:

    model = load_model(
        str(MODEL_PATH),
        compile=False,
        custom_objects={
            "DepthwiseConv2D": CompatibleDepthwiseConv2D
        }
    )

    print("AI model loaded successfully!")

except Exception as error:

    print("MODEL LOADING FAILED!")
    print(error)

    raise SystemExit(
        "Please check TensorFlow/Keras compatibility."
    )


# ==========================================
# 6. CHECK LABEL COUNT
# ==========================================

output_count = model.output_shape[-1]

if output_count != len(labels):

    raise SystemExit(
        f"ERROR: Model has {output_count} outputs "
        f"but labels.txt has {len(labels)} labels."
    )


print("Available categories:")

for label in labels:
    print("-", clean_label(label))


# ==========================================
# 7. START CAMERA
# ==========================================

print("----------------------------------")
print("Starting camera...")

camera = cv2.VideoCapture(CAMERA_INDEX)

if not camera.isOpened():

    raise SystemExit(
        "Camera not found. Try CAMERA_INDEX = 1 "
        "or check Mac camera permissions."
    )


print("Camera started!")
print("AI TEST RUNNING")
print("Press Q to quit.")
print("----------------------------------")


# ==========================================
# 8. AI CAMERA PREDICTION
# ==========================================

try:

    while True:

        ok, frame = camera.read()

        if not ok:

            print("Cannot read camera frame.")
            break


        # Convert BGR to RGB
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        # Resize image
        image = cv2.resize(
            rgb,
            IMAGE_SIZE
        )


        # Normalize image for Teachable Machine
        image = image.astype(np.float32)

        image = (image / 127.5) - 1.0


        # Add batch dimension
        image = np.expand_dims(
            image,
            axis=0
        )


        # Predict object category
        scores = model.predict(
            image,
            verbose=0
        )[0]


        # Get highest prediction
        index = int(np.argmax(scores))

        label = clean_label(labels[index])

        confidence = float(scores[index])


        # Display prediction
        display_text = (
            f"{label.upper()} - "
            f"{confidence * 100:.1f}%"
        )

        cv2.putText(
            frame,
            display_text,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


        # Display camera window
        cv2.imshow(
            "Smart Recycling Bin - AI Test",
            frame
        )


        # Quit with Q
        if cv2.waitKey(1) & 0xFF == ord("q"):

            break


finally:

    # Release camera
    camera.release()

    # Close all windows
    cv2.destroyAllWindows()

    print("AI camera test stopped.")
