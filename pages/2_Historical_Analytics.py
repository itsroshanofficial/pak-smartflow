import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Pak-SmartFlow - Historical Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Historical Traffic Analytics & Logs")
st.subheader("Overview of Past Traffic Compliance Cases")

st.markdown("---")

# Sample historical data representing past detected cases
@st.cache_data
def load_historical_data():
    data = {
        "Case ID": [101, 102, 103, 104, 105, 106],
        "Violation": ["Speeding", "Wrong Parking", "Red Light Violation", "Speeding", "Dangerous Driving", "Wrong Parking"],
        "Severity": [0.60, 0.30, 0.80, 0.60, 1.00, 0.30],
        "Risk Score": [0.65, 0.35, 0.85, 0.62, 0.95, 0.32],
        "Status": ["Reviewed - Fined", "Pending Review", "Reviewed - Warning", "Reviewed - Fined", "Escalated", "Pending Review"]
    }
    return pd.DataFrame(data)

df = load_historical_data()

st.markdown("### 📋 Recent Violation Logs")
st.dataframe(df, use_container_width=True)

st.markdown("### 📊 Risk Score Trends Across Cases")
chart_data = df.set_index("Case ID")[["Severity", "Risk Score"]]
st.bar_chart(chart_data)

st.info("💡 **Tip:** Use this historical log page to audit past decisions and monitor overall traffic safety metrics.")
