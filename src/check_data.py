import pandas as pd

# Load dataset
df = pd.read_csv("predictive_safety/traffic_safety_dataset.csv")

print("\n===== DATASET INFORMATION =====")

print("\nTotal Records:")
print(len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 10 Records:")
print(df.head(10))

print("\nRisk Level Distribution:")
print(df["risk_level"].value_counts())

print("\nAverage Values:")
print(df[[
    "speed",
    "distance",
    "sudden_braking",
    "trajectory_change",
    "traffic_density",
    "risk_score"
]].mean())