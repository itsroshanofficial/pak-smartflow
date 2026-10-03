from ultralytics import YOLO
from datetime import datetime
import json
import os

# ---------------------------------------------
# LOAD TRAINED TRAFFIC VIOLATION MODEL
# ---------------------------------------------

model = YOLO("runs/detect/train/weights/best.pt")

# ---------------------------------------------
# INPUT IMAGE
# ---------------------------------------------

image_path = "output/test_traffic.jpg"

# ---------------------------------------------
# CREATE TIMESTAMP
# ---------------------------------------------

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------------------------------------------
# RUN DETECTION
# ---------------------------------------------

results = model(image_path, conf=0.25)

# ---------------------------------------------
# OUTPUT FILE PATHS
# ---------------------------------------------

evidence_path = "output/evidence_traffic.jpg"
json_path = "output/detection_result.json"

# ---------------------------------------------
# STORE ALL DETECTIONS
# ---------------------------------------------

detections = []

for result in results:

    # -----------------------------------------
    # SAVE EVIDENCE FRAME
    # -----------------------------------------

    result.save(filename=evidence_path)

    print("\n===== TRAFFIC VIOLATION DETECTION =====")
    print(f"Timestamp: {timestamp}")

    # -----------------------------------------
    # PROCESS EACH DETECTED VIOLATION
    # -----------------------------------------

    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = model.names[class_id]

        detection_data = {
            "timestamp": timestamp,
            "violation_type": class_name,
            "detection_confidence": round(confidence, 2),
            "evidence_frame": evidence_path
        }

        detections.append(detection_data)

        # -------------------------------------
        # DISPLAY RESULT
        # -------------------------------------

        print(f"\nViolation: {class_name}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Evidence Frame: {evidence_path}")

# ---------------------------------------------
# FINAL STRUCTURED OUTPUT
# ---------------------------------------------

final_result = {
    "image": image_path,
    "timestamp": timestamp,
    "detections": detections
}

# ---------------------------------------------
# SAVE JSON
# ---------------------------------------------

with open(json_path, "w") as file:
    json.dump(
        final_result,
        file,
        indent=4
    )

print("\n===== STRUCTURED DETECTION OUTPUT =====")
print(final_result)

print(f"\nDetection JSON saved to: {json_path}")
print("\nTraffic violation detection completed successfully!")