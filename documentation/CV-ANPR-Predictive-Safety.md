Pak-SmartFlow — Computer Vision, ANPR & Predictive Road Safety
Prepared by: Musfira Jabeen
Role: Computer Vision, ANPR & Predictive Safety
1. Traffic Violation Detection
Objective
Developed a YOLO-based Computer Vision module to detect traffic violations from images and generate structured detection results.
Dataset
The traffic violation dataset contains 7 classes:
•	Illegal Overtaking
•	Illegal Parking
•	Illegal U-Turn
•	No Helmet
•	Number Plate
•	Red Light Violation
•	Traffic Light Red
The dataset was divided into training, validation, and testing sets.
Model
The trained YOLO model was saved at:
runs/detect/train/weights/best.pt
Output
The detection module provides:
•	Violation Type
•	Detection Confidence
•	Evidence Frame
•	Timestamp
During testing, the model detected 3 No Helmet and 2 Number Plate objects. The highest-confidence detection was recorded with 0.95 confidence.
Evidence was saved as:
output/final_evidence.jpg
Detection results were also stored in JSON format.
________________________________________
2. Vehicle Intelligence & ANPR
Objective
Developed an ANPR system to detect vehicle number plates and extract their registration numbers using OCR.
ANPR Model
The number plate detection model was trained using a dedicated number plate dataset.
Model:
runs/detect/train-2/weights/best.pt
OCR Processing
Tesseract OCR was used for character recognition. The detected plate is cropped, enlarged, enhanced, sharpened, and processed using thresholding techniques before OCR.
Tesseract version used: 5.5.3
Testing Results
Test 1
•	Plate Confidence: 0.93
•	Vehicle Number: 5LEF1293503
•	OCR Status: READ
Test 2
•	Plate Confidence: 0.93
•	Vehicle Number: OCR_UNREADABLE
•	OCR Status: UNREADABLE
Test 3
•	Plate Confidence: 0.92
•	OCR produced ambiguous results and was therefore not considered a verified vehicle identity.
The ANPR module saves plate crops and structured JSON results for backend integration.
________________________________________
3. Predictive Road Safety
Objective
Developed a basic predictive safety prototype to estimate traffic risk using vehicle and road conditions.
Dataset
A synthetic dataset of 500 traffic scenarios was generated with the following features:
•	Speed
•	Distance
•	Sudden Braking
•	Trajectory Change
•	Traffic Density
•	Risk Score
•	Risk Level
Risk levels were classified as LOW, MEDIUM, or HIGH.
Model
A Random Forest Classifier with 100 trees was trained using an 80/20 train-test split.
The model achieved 90% test accuracy on the synthetic dataset.
Model:
predictive_safety/predictive_safety_model.pkl
Test Scenarios
Scenario	Speed	Distance	Risk
High Risk	90 km/h	12 m	HIGH
Medium Risk	70 km/h	20 m	MEDIUM
Low Risk	40 km/h	60 m	LOW
The predictive safety result is saved in JSON format.
________________________________________
4. Final Integrated Pipeline
The three modules were combined into one pipeline:
Detection → Evidence → ANPR/OCR → Vehicle Number → Predictive Safety → Risk Level → JSON Output
The integrated pipeline was implemented in:
src/final_pipeline.py
Final Test Result
•	Violation: Number Plate
•	Detection Confidence: 0.95
•	Vehicle Number: 5LEF1293503
•	Plate Confidence: 0.93
•	OCR Status: READ
•	Risk Level: MEDIUM
•	Prediction Confidence: 85%
Final structured output:
output/final_pipeline_result.json
________________________________________
5. Files Prepared
Source Code
•	detect_traffic.py
•	anpr.py
•	anpr_ocr.py
•	final_pipeline.py
Models
•	best.pt — Traffic Detection
•	best.pt — ANPR
•	predictive_safety_model.pkl
Outputs
•	Detection JSON
•	ANPR JSON
•	Predictive Safety JSON
•	Final Pipeline JSON
•	Evidence Frame
•	Number Plate Crop
________________________________________
6. Limitations
The current system is a prototype. ANPR accuracy can be affected by image quality, lighting, angle, and plate visibility. The predictive safety model uses synthetic data, so its accuracy represents prototype performance rather than real-world accident prediction.
7. Conclusion
The assigned Computer Vision, ANPR, and Predictive Road Safety modules were successfully developed and tested. The final pipeline produces structured outputs containing violation information, evidence, vehicle number, and safety risk, making the results ready for further backend integration.
