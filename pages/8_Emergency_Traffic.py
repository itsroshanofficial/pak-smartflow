import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from ui import inject_css, hero, kpi, disclaimer, RED, CYAN, GREEN, AMBER

st.set_page_config(page_title="Emergency & Traffic · Pak-SmartFlow", page_icon="🚑", layout="wide")
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
    "🚑 Emergency Green Corridor & Traffic Optimization",
    "Dynamic signal clearing for ambulances and real-time urban traffic flow optimization.",
    [("AGENT 9", RED), ("AGENT 10", CYAN)]
)

c1, c2 = st.columns(2)

with c1:
    st.markdown("### 🚑 Active Emergency Corridor")
    st.info("Ambulance ID: AMB-789 (Rescue 1122)\nRoute: Jail Road → Services Hospital\nStatus: Corridors Cleared (Green wave active)")
    if st.button("🚨 Trigger Emergency Override", use_container_width=True):
        st.success("Signals synchronized along the route successfully!")

with c2:
    st.markdown("### 🚦 Intersection Signal Optimizer")
    st.metric("Current Traffic Flow Efficiency", "+34.5%", "vs fixed timers")
    st.slider("Adjust Green Light Duration (sec)", 30, 120, 60)

disclaimer()
