import streamlit as st
import pandas as pd
from pak_smartflow_engine import pak_smartflow_engine

st.set_page_config(
    page_title="Pak-SmartFlow - Live Analysis",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 Pak-SmartFlow: Live Traffic Analysis")
st.subheader("AI-Powered Multi-Agent Traffic Intelligence System")

st.info(
    "Prototype using synthetic data. "
    "Any enforcement decision requires human review."
)

st.header("Vehicle & Traffic Inputs")

col1, col2 = st.columns(2)

with col1:
    confidence = st.number_input(
        "Detection Confidence", 0.0, 1.0, 0.95, 0.01
    )
    safety_risk = st.number_input(
        "Safety Risk", 0.0, 1.0, 0.50, 0.01
    )
    traffic_density = st.number_input(
        "Traffic Density", 0.0, 1.0, 0.50, 0.01
    )
    vehicle_history = st.number_input(
        "Vehicle History", 0.0, 1.0, 0.30, 0.01
    )

with col2:
    predicted_risk = st.number_input(
        "Predicted Risk", 0.0, 1.0, 0.40, 0.01
    )
    compliance = st.number_input(
        "Compliance Score", 0.0, 1.0, 0.70, 0.01
    )
    violation = st.selectbox(
        "Detected Violation",
        [
            "No Violation",
            "Wrong Parking",
            "Speeding",
            "Red Light Violation",
            "Dangerous Driving"
        ]
    )

severity_map = {
    "No Violation": 0.00,
    "Wrong Parking": 0.30,
    "Speeding": 0.60,
    "Red Light Violation": 0.80,
    "Dangerous Driving": 1.00
}

severity = severity_map[violation]
st.write("Illustrative Severity Score:", severity)

if st.button("Analyze Traffic Case"):
    result = pak_smartflow_engine(
        confidence,
        severity,
        safety_risk,
        traffic_density,
        vehicle_history,
        predicted_risk,
        compliance
    )

    st.header("Decision Engine Results")

    a, b, c = st.columns(3)
    a.metric("Risk Score", result["Risk Score"])
    b.metric("Fuzzy Decision Score", result["Fuzzy Decision Score"])
    c.metric("Final Decision Score", result["Final Decision Score"])

    st.subheader("Fuzzy Membership")
    st.write("Low Risk:", result["Low Membership"])
    st.write("Medium Risk:", result["Medium Membership"])
    st.write("High Risk:", result["High Membership"])

    st.subheader("RecommendedAction")
    st.success(result["Recommended Action"])

    report_data = pd.DataFrame([{
        "Violation": violation,
        "Detection Confidence": confidence,
        "Severity Score": severity,
        "Safety Risk": safety_risk,
        "Traffic Density": traffic_density,
        "Vehicle History": vehicle_history,
        "Predicted Risk": predicted_risk,
        "Compliance Score": compliance,
        "Risk Score": result["Risk Score"],
        "Fuzzy Decision Score": result["Fuzzy Decision Score"],
        "Final Decision Score": result["Final Decision Score"],
        "Recommended Action": result["Recommended Action"]
    }])

    csv = report_data.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Analysis Report (CSV)",
        data=csv,
        file_name="pak_smartflow_report.csv",
        mime="text/csv",
    )

    st.warning(
        "Prototype recommendation only. Human review is required "
        "before any enforcement action."
    )
