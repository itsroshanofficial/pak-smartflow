import streamlit as st
import pandas as pd
import time
import streamlit.components.v1 as components
from ui import inject_css, hero, disclaimer, back_to_home, RED, CYAN, GREEN, AMBER

st.set_page_config(
    page_title="Pak-SmartFlow - Alert System",
    page_icon="🚨",
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
    "🚨 Automated Alert Dispatch Module",
    "Simulate Real-Time SMS & Email Dispatches for High-Risk Traffic Violations",
    [("DISPATCH SYSTEM", RED), ("REAL-TIME ALERTS", AMBER)]
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📋 Violation Alert Parameters")
    vehicle_reg = st.text_input("Vehicle Registration Number", "LEA-2026-9871")
    owner_phone = st.text_input("Owner Mobile Number (+92)", "+92 300 1234567")
    owner_email = st.text_input("Owner Email Address", "citizen@example.com")
    
    violation_type = st.selectbox(
        "Severity Level / Violation",
        ["Dangerous Driving (High Risk)", "Red Light Violation (High Risk)", "Speeding (Medium Risk)", "Wrong Parking (Low Risk)"]
    )

with col2:
    st.markdown("### 📡 Dispatch Channels")
    send_sms = st.checkbox("Send SMS Notification", value=True)
    send_email = st.checkbox("Send Digital Notice (Email)", value=True)
    dispatch_authority = st.checkbox("Alert Nearest Traffic Control Unit", value=True)
    
    urgency = st.radio("Notification Priority", ["Normal", "Urgent / Immediate Action"])

st.markdown("---")

if st.button("🚀 Dispatch Automated Alert", use_container_width=True):
    with st.spinner("Connecting to National Traffic Gateway & Dispatching..."):
        time.sleep(1.5)  # Simulate network latency
        
    st.success("✅ Alert successfully dispatched across selected channels!")
    
    # Display dispatch summary metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("SMS Status", "Delivered" if send_sms else "Skipped")
    m2.metric("Email Status", "Sent" if send_email else "Skipped")
    m3.metric("Authority Log", "Logged & Synced" if dispatch_authority else "Skipped")
    
    # Log export
    alert_log = pd.DataFrame([{
        "Vehicle": vehicle_reg,
        "Phone": owner_phone,
        "Email": owner_email,
        "Violation": violation_type,
        "SMS Sent": send_sms,
        "Email Sent": send_email,
        "Priority": urgency
    }])
    
    csv = alert_log.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Dispatch Audit Log (CSV)",
        data=csv,
        file_name="pak_smartflow_alert_log.csv",
        mime="text/csv",
        use_container_width=True
    )

st.info("💡 **Note:** This simulation demonstrates automated emergency and fine notification dispatches to vehicle owners and control units.")
back_to_home()
disclaimer()
