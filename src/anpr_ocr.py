from ultralytics import YOLO
import cv2
import pytesseract
import re
import json
from datetime import datetime


# =========================================================
# TESSERACT CONFIGURATION
# =========================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# =========================================================
# LOAD TRAINED NUMBER PLATE MODEL
# =========================================================

model = YOLO("runs/detect/train-2/weights/best.pt")


# =========================================================
# INPUT IMAGE
# =========================================================

image_path = (
    "data/number_plates/test/images/"
    "DSC_0399_jpg.rf.1b4fc3c99e633602eda83ca55abd79fb.jpg"
)

image = cv2.imread(image_path)

if image is None:
    print("ERROR: Input image could not be loaded.")
    exit()


# =========================================================
# TIMESTAMP
# =========================================================

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =========================================================
# NUMBER PLATE DETECTION
# =========================================================

results = model(image, conf=0.20)


print("\n======================================")
print("       ANPR + OCR RESULTS")
print("======================================")
print(f"Timestamp: {timestamp}")


# =========================================================
# PROCESS DETECTED PLATES
# =========================================================

for result in results:

    if len(result.boxes) == 0:

        print("\nNo number plate detected.")

        result_data = {
            "timestamp": timestamp,
            "vehicle_number": "NOT_DETECTED",
            "plate_confidence": 0.0,
            "plate_crop": None,
            "ocr_status": "NOT_DETECTED"
        }

        json_path = "output/anpr_result.json"

        with open(json_path, "w") as file:
            json.dump(result_data, file, indent=4)

        print(f"ANPR JSON saved to: {json_path}")

        continue


    # =====================================================
    # PROCESS EACH DETECTED PLATE
    # =====================================================

    for plate_index, box in enumerate(result.boxes):

        confidence = float(box.conf[0])


        # =================================================
        # PLATE COORDINATES
        # =================================================

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        padding = 8

        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(image.shape[1], x2 + padding)
        y2 = min(image.shape[0], y2 + padding)


        # =================================================
        # PLATE CROP
        # =================================================

        plate = image[y1:y2, x1:x2]

        crop_path = f"output/anpr_plate_{plate_index}.jpg"

        cv2.imwrite(crop_path, plate)


        print(f"\nPlate Confidence: {confidence:.2f}")
        print(f"Plate Crop: {crop_path}")


        # =================================================
        # CREATE ORIENTATIONS
        # =================================================

        normal = plate

        rotated = cv2.rotate(
            plate,
            cv2.ROTATE_180
        )

        orientations = {
            "normal": normal,
            "rotated": rotated
        }


        # =================================================
        # OCR CANDIDATES
        # =================================================

        candidates = []


        # =================================================
        # OCR PROCESSING
        # =================================================

        for orientation_name, current_plate in orientations.items():

            # ---------------------------------------------
            # UPSCALE
            # ---------------------------------------------

            enlarged = cv2.resize(
                current_plate,
                None,
                fx=12,
                fy=12,
                interpolation=cv2.INTER_CUBIC
            )


            # ---------------------------------------------
            # GRAYSCALE
            # ---------------------------------------------

            gray = cv2.cvtColor(
                enlarged,
                cv2.COLOR_BGR2GRAY
            )


            # ---------------------------------------------
            # CONTRAST ENHANCEMENT
            # ---------------------------------------------

            clahe = cv2.createCLAHE(
                clipLimit=2.0,
                tileGridSize=(8, 8)
            )

            enhanced = clahe.apply(gray)


            # ---------------------------------------------
            # SHARPEN
            # ---------------------------------------------

            kernel = (
                0, -1, 0,
                -1, 5, -1,
                0, -1, 0
            )

            sharpened = cv2.filter2D(
                enhanced,
                -1,
                kernel
            )


            # ---------------------------------------------
            # OTSU THRESHOLD
            # ---------------------------------------------

            _, otsu = cv2.threshold(
                sharpened,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )


            # ---------------------------------------------
            # ADAPTIVE THRESHOLD
            # ---------------------------------------------

            adaptive = cv2.adaptiveThreshold(
                sharpened,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                31,
                11
            )


            # ---------------------------------------------
            # INVERTED OTSU
            # ---------------------------------------------

            _, inverted = cv2.threshold(
                sharpened,
                0,
                255,
                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )


            # ---------------------------------------------
            # IMAGES FOR OCR
            # ---------------------------------------------

            processed_images = {
                "enhanced": enhanced,
                "sharpened": sharpened,
                "otsu": otsu,
                "adaptive": adaptive,
                "inverted": inverted
            }


            # ---------------------------------------------
            # SAVE SHARPENED IMAGE
            # ---------------------------------------------

            cv2.imwrite(
                f"output/anpr_{orientation_name}_{plate_index}.jpg",
                sharpened
            )


            # ---------------------------------------------
            # TESSERACT CONFIGURATIONS
            # ---------------------------------------------

            configs = [
                "--psm 6",
                "--psm 7",
                "--psm 8",
                "--psm 13"
            ]


            # ---------------------------------------------
            # RUN OCR
            # ---------------------------------------------

            for process_name, processed_image in processed_images.items():

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


                    # -------------------------------------
                    # CLEAN OCR TEXT
                    # -------------------------------------

                    clean_text = re.sub(
                        r"[^A-Z0-9]",
                        "",
                        raw_text.upper()
                    )


                    # -------------------------------------
                    # SAVE NON-EMPTY CANDIDATES
                    # -------------------------------------

                    if clean_text:

                        candidates.append({
                            "text": clean_text,
                            "orientation": orientation_name,
                            "processing": process_name,
                            "config": config
                        })


        # =================================================
        # FILTER OCR RESULTS
        # =================================================

        valid_candidates = []

        for candidate in candidates:

            text = candidate["text"]

            # Ignore very short results such as:
            # A, S, 2, LS

            if len(text) < 4:
                continue

            # Ignore extremely long OCR garbage

            if len(text) > 12:
                continue

            valid_candidates.append(candidate)


        # =================================================
        # SELECT BEST OCR RESULT
        # =================================================

        vehicle_number = "OCR_UNREADABLE"


        if valid_candidates:

            text_counts = {}

            for candidate in valid_candidates:

                text = candidate["text"]

                if text not in text_counts:
                    text_counts[text] = 0

                text_counts[text] += 1


            # Select most repeated valid result
            # If frequency is same, prefer longer text

            vehicle_number = max(
                text_counts,
                key=lambda x: (
                    text_counts[x],
                    len(x)
                )
            )


        # =================================================
        # OCR STATUS
        # =================================================

        if vehicle_number == "OCR_UNREADABLE":
            ocr_status = "UNREADABLE"
        else:
            ocr_status = "READ"


        # =================================================
        # FINAL STRUCTURED RESULT
        # =================================================

        result_data = {
            "timestamp": timestamp,
            "vehicle_number": vehicle_number,
            "plate_confidence": round(confidence, 2),
            "plate_crop": crop_path,
            "ocr_status": ocr_status,
            "ocr_candidates": valid_candidates
        }


        # =================================================
        # DISPLAY OCR RESULT
        # =================================================

        print("\n===== OCR RESULT =====")


        if valid_candidates:

            print("Valid OCR Candidates:")

            for candidate in valid_candidates:

                print(
                    f"  {candidate['text']} "
                    f"({candidate['orientation']}, "
                    f"{candidate['processing']}, "
                    f"{candidate['config']})"
                )

        else:

            print("Valid OCR Candidates: None")


        print(f"\nVehicle Number: {vehicle_number}")
        print(f"OCR Status: {ocr_status}")


        # =================================================
        # SAVE JSON
        # =================================================

        json_path = (
            f"output/anpr_result_{plate_index}.json"
        )

        with open(json_path, "w") as file:

            json.dump(
                result_data,
                file,
                indent=4
            )


        print(
            f"ANPR JSON saved to: {json_path}"
        )


# =========================================================
# COMPLETION
# =========================================================

print("\n======================================")
print("ANPR + OCR completed successfully!")
print("======================================")