from ultralytics import YOLO
import cv2
import pytesseract

# Tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# YOLO model
model = YOLO("runs/detect/train/weights/best.pt")

# Input image
image_path = "output/test_traffic.jpg"
image = cv2.imread(image_path)

# Detect number plate
results = model(image, conf=0.25)

print("\nANPR Results:")

for result in results:

    for i, box in enumerate(result.boxes):

        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])

        if class_name.lower() == "number plate":

            # Coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Crop plate
            plate = image[y1:y2, x1:x2]

            # Save original crop
            cv2.imwrite(f"output/plate_{i}.jpg", plate)

            # -------------------------
            # OCR PREPROCESSING
            # -------------------------

            # Make plate bigger
            plate = cv2.resize(
                plate,
                None,
                fx=4,
                fy=4,
                interpolation=cv2.INTER_CUBIC
            )

            # Convert to grayscale
            gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)

            # Improve contrast
            _, processed = cv2.threshold(
                gray,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )

            # Save processed plate
            cv2.imwrite(
                f"output/plate_processed_{i}.jpg",
                processed
            )

            # OCR
            text = pytesseract.image_to_string(
                processed,
                config="--psm 7"
            ).strip()

            print(f"Plate Crop: output/plate_{i}.jpg")
            print(f"Processed Plate: output/plate_processed_{i}.jpg")
            print(f"Detection Confidence: {confidence:.2f}")
            print(f"Vehicle Number: {text}")