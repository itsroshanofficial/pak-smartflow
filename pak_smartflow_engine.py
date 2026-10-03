
def validate_score(value, name):
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1.")
    return value


def fuzzy_membership(risk):
    if risk <= 0.30:
        low = 1.0
    elif risk >= 0.50:
        low = 0.0
    else:
        low = (0.50 - risk) / 0.20

    if risk <= 0.30 or risk >= 0.80:
        medium = 0.0
    elif risk <= 0.55:
        medium = (risk - 0.30) / 0.25
    else:
        medium = (0.80 - risk) / 0.25

    if risk <= 0.60:
        high = 0.0
    elif risk >= 0.80:
        high = 1.0
    else:
        high = (risk - 0.60) / 0.20

    return round(low, 3), round(medium, 3), round(high, 3)


def final_action(score):
    if score < 0.30:
        return "Information / Warning"
    elif score < 0.60:
        return "Notification / Human Review"
    else:
        return "Simulated Enforcement Request / Human Review"


def pak_smartflow_engine(
    confidence, severity, safety_risk,
    traffic_density, vehicle_history,
    predicted_risk, compliance
):
    inputs = {
        "Confidence": confidence,
        "Severity": severity,
        "Safety Risk": safety_risk,
        "Traffic Density": traffic_density,
        "Vehicle History": vehicle_history,
        "Predicted Risk": predicted_risk,
        "Compliance": compliance
    }

    for name, value in inputs.items():
        validate_score(value, name)

    risk = (
        0.15 * confidence
        + 0.20 * severity
        + 0.25 * safety_risk
        + 0.10 * traffic_density
        + 0.10 * vehicle_history
        + 0.20 * predicted_risk
    )
    risk = round(risk, 3)

    low, medium, high = fuzzy_membership(risk)

    fuzzy_decision = round(
        0.20 * low + 0.60 * medium + 1.00 * high, 3
    )

    final_score = round(
        0.70 * fuzzy_decision + 0.30 * (1 - compliance), 3
    )

    return {
        "Risk Score": risk,
        "Low Membership": low,
        "Medium Membership": medium,
        "High Membership": high,
        "Fuzzy Decision Score": fuzzy_decision,
        "Compliance Score": compliance,
        "Final Decision Score": final_score,
        "Recommended Action": final_action(final_score)
    }
