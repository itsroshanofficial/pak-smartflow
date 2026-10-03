import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from ui import inject_css, hero, disclaimer, back_to_home, SHADE, CYAN, AMBER, GREEN, RED

st.set_page_config(
    page_title="Pak-SmartFlow - Compliance & Enforcement",
    page_icon="🛡️",
    layout="wide"
)
inject_css()

# Professional Navigation Buttons
col_back, col_home = st.columns([1, 4])
with col_back:
    components.html("""
        <div style="padding-top: 2px;">
            <button onclick="window.history.back()" style="background: rgba(20,38,59,0.8); color: #38BDF8; border: 1px solid rgba(56,189,248,0.4); padding: 6px 14px; border-radius: 8px; cursor: pointer; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 13px;">
                ⬅ Back
            </button>
        </div>
    """, height=45)
with col_home:
    st.page_link("app.py", label="Go to Main Dashboard", icon="🏠")

st.write("")

hero(
    "🛡️ Agent 11 & 12: Compliance & Enforcement Escalation",
    "Persistent Default Tracking & Traffic Department Review Workflow",
    [("AGENT 11", AMBER), ("AGENT 12", GREEN)]
)

st.markdown("### 📊 Active Compliance Monitoring Queue")

# Mock DataFrame representing persistent defaults and compliance scores
compliance_data = pd.DataFrame([
    {"Vehicle": "LEA-2026-9871", "Unpaid Challans": 3, "Total Amount (PKR)": 12500, "Compliance Score": 0.35, "Status": "Escalated for Review"},
    {"Vehicle": "RSP-2025-4412", "Unpaid Challans": 1, "Total Amount (PKR)": 2500, "Compliance Score": 0.75, "Status": "Warning Sent"},
    {"Vehicle": "ISB-2024-8890", "Unpaid Challans": 5, "Total Amount (PKR)": 24000, "Compliance Score": 0.15, "Status": "Enforcement Requested"}
])

st.dataframe(compliance_data, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("### 🏛️ Authority Review Simulation (Traffic Department)")

selected_vehicle = st.selectbox("Select Case for Review", compliance_data["Vehicle"])
selected_row = compliance_data[compliance_data["Vehicle"] == selected_vehicle].iloc[0]

st.write(f"**Reviewing Case for Vehicle:** {selected_vehicle} | **Total Dues:** PKR {selected_row['Total Amount (PKR)']} | **Compliance Score:** {selected_row['Compliance Score']}")

review_action = st.radio("Authority Decision", ["Approve Enforcement Request", "Grant Extension / Payment Plan", "Reject & Dismiss"])

if st.button("⚖️ Execute Authority Decision", use_container_width=True):
    if review_action == "Approve Enforcement Request":
        st.error(f"🚨 Enforcement Request Approved! Formal notice dispatched to Traffic Control Unit for vehicle {selected_vehicle}.")
    elif review_action == "Grant Extension / Payment Plan":
        st.warning(f"🤝 Payment assistance and 15-day extension granted for vehicle {selected_vehicle}.")
    else:
        st.success(f"✅ Case dismissed and compliance restored for vehicle {selected_vehicle}.")

back_to_home()
disclaimer()
