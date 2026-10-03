import joblib
import json
import os
import pandas as pd
from datetime import datetime

# Load trained model
model = joblib.load("predictive_safety/predictive_safety_model.pkl")

print("Predictive Safety Model loaded successfully!")

# ==============================
# INPUT TRAFFIC SCENARIO
# ==============================

speed = 70
distance = 20
sudden_braking = 1
trajectory_change = 0
traffic_density = 2

density_names = {
    1: "LOW",
    2: "MEDIUM",
    3: "HIGH"
}

# ==============================
# MODEL PREDICTION
# ==============================

input_data = pd.DataFrame([{
    "speed": speed,
    "distance": distance,
    "sudden_braking": sudden_braking,
    "trajectory_change": trajectory_change,
    "traffic_density": traffic_density
}])

prediction = model.predict(input_data)[0]

probabilities = model.predict_proba(input_data)[0]
confidence = max(probabilities) * 100

# ==============================
# EXPLANATION
# ==============================

reasons = []

if speed >= 80:
    reasons.append("high vehicle speed")
elif speed >= 60:
    reasons.append("elevated vehicle speed")

if distance <= 15:
    reasons.append("very short following distance")
elif distance <= 30:
    reasons.append("short following distance")

if sudden_braking == 1:
    reasons.append("sudden braking detected")

if trajectory_change == 1:
    reasons.append("trajectory change detected")

if traffic_density == 3:
    reasons.append("high traffic density")

if reasons:
    reason_text = ", ".join(reasons)
else:
    reason_text = "No major risk indicators detected"

# ==============================
# RECOMMENDED ACTION
# ==============================

if prediction == "HIGH":
    action = "Flag for immediate safety monitoring and alert authorized traffic operators."

elif prediction == "MEDIUM":
    action = "Flag for closer monitoring."

else:
    action = "Continue normal monitoring."

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ==============================
# DISPLAY RESULT
# ==============================

print("\n===== PREDICTIVE ROAD SAFETY =====")

print(f"Timestamp: {timestamp}")
print(f"Speed: {speed} km/h")
print(f"Distance: {distance} meters")
print(f"Sudden Braking: {'YES' if sudden_braking else 'NO'}")
print(f"Trajectory Change: {'YES' if trajectory_change else 'NO'}")
print(f"Traffic Density: {density_names[traffic_density]}")

print(f"\nPredicted Risk Level: {prediction}")
print(f"Prediction Confidence: {confidence:.2f}%")

print(f"\nRisk Indicators: {reason_text}")
print(f"Recommended Action: {action}")

if prediction == "HIGH":
    print("\nWARNING: HIGH ROAD SAFETY RISK")

# ==============================
# STRUCTURED JSON OUTPUT
# ==============================

result = { 
    "timestamp": timestamp,
    "risk_level": prediction,
    "risk_confidence": round(confidence, 2),
    "speed_kmh": speed,
    "distance_m": distance,
    "sudden_braking": bool(sudden_braking),
    "trajectory_change": bool(trajectory_change),
    "traffic_density": density_names[traffic_density],
    "risk_indicators": reasons,
    "recommended_action": action
}

# Create output folder if needed
os.makedirs("output", exist_ok=True)

# Save JSON result
json_path = "output/predictive_safety_result.json"

with open(json_path, "w") as file:
    json.dump(result, file, indent=4)

print(f"\nStructured result saved to: {json_path}")
print("\nPredictive Safety completed successfully!")