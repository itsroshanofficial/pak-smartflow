import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv(
    "predictive_safety/traffic_safety_dataset.csv"
)

print("Dataset loaded successfully!")
print("Total records:", len(df))


# ==========================================
# 2. INPUT FEATURES
# ==========================================

X = df[
    [
        "speed",
        "distance",
        "sudden_braking",
        "trajectory_change",
        "traffic_density"
    ]
]


# ==========================================
# 3. TARGET
# ==========================================

y = df["risk_level"]


# ==========================================
# 4. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ==========================================
# 5. CREATE MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# ==========================================
# 6. TRAIN MODEL
# ==========================================

model.fit(X_train, y_train)

print("\nModel training completed!")


# ==========================================
# 7. MAKE PREDICTIONS
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# 8. EVALUATE MODEL
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n===== MODEL PERFORMANCE =====")
print(f"Accuracy: {accuracy:.2%}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)

# ==========================================
# 9. SAVE TRAINED MODEL
# ==========================================

joblib.dump(
    model,
    "predictive_safety/predictive_safety_model.pkl"
)

print("\nTrained model saved successfully!")