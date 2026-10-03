from ultralytics import YOLO
import cv2
import pytesseract
import re
import json
from datetime import datetime
import pandas as pd
import joblib


# =========================================================
# CONFIGURATION
# =========================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

IMAGE_PATH = (
    "data/number_plates/test/images/"
    "DSC_0329_jpg.rf.e290fd79a0d3e95ee25d266337683c07.jpg"
)

DETECTION_MODEL = "runs/detect/train/weights/best.pt"
ANPR_MODEL = "runs/detect/train-2/weights/best.pt"
SAFETY_MODEL = "predictive_safety/predictive_safety_model.pkl"


# =========================================================
# LOAD IMAGE
# =========================================================

image = cv2.imread(IMAGE_PATH)

if image is None:
    print("ERROR: Image could not be loaded.")
    exit()

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


print("\n==============================================")
print("       PAK-SMARTFLOW FINAL PIPELINE")
print("==============================================")
print(f"Timestamp: {timestamp}")
print(f"Input Image: {IMAGE_PATH}")


# =========================================================
# AGENT 1 — TRAFFIC DETECTION
# =========================================================

print("\n==============================================")
print("        AGENT 1 — DETECTION")
print("==============================================")

detection_model = YOLO(DETECTION_MODEL)

detection_results = detection_model(
    image,
    conf=0.25
)

violation_type = "NOT_DETECTED"
detection_confidence = 0.0
evidence_path = None

for result in detection_results:

    if len(result.boxes) > 0:

        result.save(
            filename="output/final_evidence.jpg"
        )

        evidence_path = "output/final_evidence.jpg"

        # Take highest-confidence detection
        best_box = max(
            result.boxes,
            key=lambda box: float(box.conf[0])
        )

        class_id = int(best_box.cls[0])
        detection_confidence = float(
            best_box.conf[0]
        )

        violation_type = detection_model.names[
            class_id
        ]

        print(f"Violation: {violation_type}")
        print(
            f"Detection Confidence: "
            f"{detection_confidence:.2f}"
        )
        print(f"Evidence: {evidence_path}")

    else:

        print("No traffic violation detected.")


# =========================================================
# AGENT 2 — ANPR + OCR
# =========================================================

print("\n==============================================")
print("        AGENT 2 — ANPR / OCR")
print("==============================================")

anpr_model = YOLO(ANPR_MODEL)

anpr_results = anpr_model(
    image,
    conf=0.20
)

vehicle_number = "NOT_DETECTED"
plate_confidence = 0.0
ocr_status = "NOT_DETECTED"
plate_crop_path = None

for result in anpr_results:

    if len(result.boxes) == 0:

        print("Number plate not detected.")

        continue

    # Highest-confidence plate
    best_plate = max(
        result.boxes,
        key=lambda box: float(box.conf[0])
    )

    plate_confidence = float(
        best_plate.conf[0]
    )

    x1, y1, x2, y2 = map(
        int,
        best_plate.xyxy[0]
    )

    padding = 8

    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(image.shape[1], x2 + padding)
    y2 = min(image.shape[0], y2 + padding)

    plate = image[y1:y2, x1:x2]

    plate_crop_path = (
        "output/final_plate_crop.jpg"
    )

    cv2.imwrite(
        plate_crop_path,
        plate
    )

    print(
        f"Plate Confidence: "
        f"{plate_confidence:.2f}"
    )

    print(
        f"Plate Crop: "
        f"{plate_crop_path}"
    )


    # -----------------------------------------------------
    # OCR
    # -----------------------------------------------------

    enlarged = cv2.resize(
        plate,
        None,
        fx=12,
        fy=12,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.cvtColor(
        enlarged,
        cv2.COLOR_BGR2GRAY
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    sharpen_kernel = (
        0, -1, 0,
        -1, 5, -1,
        0, -1, 0
    )

    sharpened = cv2.filter2D(
        enhanced,
        -1,
        sharpen_kernel
    )

    _, otsu = cv2.threshold(
        sharpened,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    adaptive = cv2.adaptiveThreshold(
        sharpened,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    processed_images = [
        enhanced,
        sharpened,
        otsu,
        adaptive
    ]

    configs = [
        "--psm 6",
        "--psm 7",
        "--psm 8",
        "--psm 13"
    ]

    candidates = []

    for processed_image in processed_images:

        for config in configs:

            raw_text = pytesseract.image_to_string(
                processed_image,
                config=(
                    config
                    + " -c "
                    "tessedit_char_whitelist="
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                )
            )

            clean_text = re.sub(
                r"[^A-Z0-9]",
                "",
                raw_text.upper()
            )

            # Reject obvious garbage
            if 4 <= len(clean_text) <= 12:

                candidates.append(
                    clean_text
                )


    # -----------------------------------------------------
    # SELECT OCR RESULT
    # -----------------------------------------------------

    if candidates:

        counts = {}

        for text in candidates:
            counts[text] = (
                counts.get(text, 0) + 1
            )

        vehicle_number = max(
            counts,
            key=lambda x: (
                counts[x],
                len(x)
            )
        )

        ocr_status = "READ"

    else:

        vehicle_number = "OCR_UNREADABLE"
        ocr_status = "UNREADABLE"


    print(
        f"Vehicle Number: "
        f"{vehicle_number}"
    )

    print(
        f"OCR Status: "
        f"{ocr_status}"
    )


# =========================================================
# AGENT 5 — PREDICTIVE ROAD SAFETY
# =========================================================

print("\n==============================================")
print("      AGENT 5 — PREDICTIVE ROAD SAFETY")
print("==============================================")

safety_model = joblib.load(
    SAFETY_MODEL
)


# Prototype scenario
# These values can later come from video analytics.

speed = 70
distance = 20
sudden_braking = 1
trajectory_change = 0
traffic_density = 2


safety_input = pd.DataFrame(
    [[
        speed,
        distance,
        sudden_braking,
        trajectory_change,
        traffic_density
    ]],
    columns=[
        "speed",
        "distance",
        "sudden_braking",
        "trajectory_change",
        "traffic_density"
    ]
)


risk_prediction = safety_model.predict(
    safety_input
)[0]

risk_probabilities = (
    safety_model.predict_proba(
        safety_input
    )[0]
)

risk_confidence = (
    max(risk_probabilities) * 100
)


print(f"Speed: {speed} km/h")
print(f"Distance: {distance} meters")
print(
    f"Sudden Braking: "
    f"{'YES' if sudden_braking else 'NO'}"
)
print(
    f"Trajectory Change: "
    f"{'YES' if trajectory_change else 'NO'}"
)

print(
    f"Predicted Risk Level: "
    f"{risk_prediction}"
)

print(
    f"Prediction Confidence: "
    f"{risk_confidence:.2f}%"
)


# =========================================================
# FINAL COMBINED RESULT
# =========================================================

final_result = {

    "timestamp": timestamp,

    "input_image": IMAGE_PATH,

    "detection": {

        "violation_type": violation_type,

        "detection_confidence": round(
            detection_confidence,
            2
        ),

        "evidence_frame": evidence_path

    },

    "anpr": {

        "vehicle_number": vehicle_number,

        "plate_confidence": round(
            plate_confidence,
            2
        ),

        "plate_crop": plate_crop_path,

        "ocr_status": ocr_status

    },

    "predictive_safety": {

        "speed_kmh": speed,

        "distance_meters": distance,

        "sudden_braking": bool(
            sudden_braking
        ),

        "trajectory_change": bool(
            trajectory_change
        ),

        "traffic_density": traffic_density,

        "risk_level": str(
            risk_prediction
        ),

        "prediction_confidence": round(
            risk_confidence,
            2
        )

    }

}


# =========================================================
# SAVE FINAL JSON
# =========================================================

json_path = (
    "output/final_pipeline_result.json"
)

with open(
    json_path,
    "w"
) as file:

    json.dump(
        final_result,
        file,
        indent=4
    )


# =========================================================
# FINAL DISPLAY
# =========================================================

print("\n==============================================")
print("       FINAL PAK-SMARTFLOW OUTPUT")
print("==============================================")

print(
    json.dumps(
        final_result,
        indent=4
    )
)

print("\nFinal JSON saved to:")
print(json_path)

print("\n==============================================")
print("       FINAL PIPELINE COMPLETED")
print("==============================================")