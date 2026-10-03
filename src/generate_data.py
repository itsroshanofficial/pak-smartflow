import pandas as pd
import random

# Number of traffic scenarios
NUM_SAMPLES = 500

data = []

for _ in range(NUM_SAMPLES):

    # Vehicle speed: 20 to 120 km/h
    speed = random.randint(20, 120)

    # Distance from vehicle ahead: 5 to 100 meters
    distance = random.randint(5, 100)

    # Sudden braking: 0 = No, 1 = Yes
    sudden_braking = random.randint(0, 1)

    # Trajectory change: 0 = No, 1 = Yes
    trajectory_change = random.randint(0, 1)

    # Traffic density: 1 = Low, 2 = Medium, 3 = High
    traffic_density = random.randint(1, 3)

    # -----------------------------
    # Risk Score Calculation
    # -----------------------------

    risk_score = 0

    # Speed factor
    if speed >= 80:
        risk_score += 2
    elif speed >= 60:
        risk_score += 1

    # Distance factor
    if distance <= 15:
        risk_score += 2
    elif distance <= 30:
        risk_score += 1

    # Sudden braking
    if sudden_braking == 1:
        risk_score += 2

    # Trajectory change
    if trajectory_change == 1:
        risk_score += 1

    # Traffic density
    if traffic_density == 3:
        risk_score += 1

    # -----------------------------
    # Risk Level
    # -----------------------------

    if risk_score >= 5:
        risk_level = "HIGH"

    elif risk_score >= 3:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    data.append([
        speed,
        distance,
        sudden_braking,
        trajectory_change,
        traffic_density,
        risk_score,
        risk_level
    ])


# Create DataFrame
df = pd.DataFrame(
    data,
    columns=[
        "speed",
        "distance",
        "sudden_braking",
        "trajectory_change",
        "traffic_density",
        "risk_score",
        "risk_level"
    ]
)

# Save dataset
df.to_csv(
    "predictive_safety/traffic_safety_dataset.csv",
    index=False
)

print("Synthetic traffic dataset generated successfully!")
print(f"Total scenarios: {len(df)}")
print("\nFirst 10 records:")
print(df.head(10))