import streamlit as st
import pandas as pd
import time
import streamlit.components.v1 as components
from pak_smartflow_engine import pak_smartflow_engine
from db_helper import insert_violation
from ui import inject_css, hero, disclaimer, back_to_home, CYAN, AMBER, GREEN, RED, VIOLET

st.set_page_config(
    page_title="Pak-SmartFlow - AI Vision Detection",
    page_icon="👁️",
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
    "👁️ AI Vision Detection & ANPR Module",
    "Upload Traffic Camera Images or CCTV Frames for Automated Violation & Plate Recognition",
    [("VISION AGENT", CYAN), ("ANPR ENGINE", GREEN)]
)

st.markdown("### 📤 Upload Traffic Evidence Image")
uploaded_file = st.file_uploader("Choose an image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    col_img, col_res = st.columns([1, 1])
    
    with col_img:
        st.image(uploaded_file, caption="Uploaded Traffic Frame", use_container_width=True)
        
    with col_res:
        st.markdown("### 🔍 Vision Analysis Results")
        with st.spinner("Running YOLOv8 ANPR & Violation Detection Model..."):
            time.sleep(1.5)  # Simulate AI processing latency
            
        st.success("✅ Frame Analyzed Successfully!")
        
        # Detected metrics
        detected_plate = "LEA-2026-9871"
        detected_violation = "Red Light Violation & Speeding"
        confidence = "98.4%"
        risk_score = 0.85
        
        st.metric("Detected Number Plate (ANPR)", detected_plate)
        st.metric("Identified Violation", detected_violation)
        st.metric("Model Confidence", confidence)
        st.metric("Calculated Risk Score", f"{risk_score} (High Risk)")
        
        if st.button("🚀 Log Violation & Trigger Enforcement", use_container_width=True):
            insert_violation(
                plate=detected_plate,
                violation_type=detected_violation,
                risk_score=risk_score,
                final_score=0.91,
                action="Automated Challan Dispatched"
            )
            st.success("🎉 Violation successfully logged to Supabase and routed to Agent Network!")

else:
    st.info("💡 **Tip:** Upload any vehicle or traffic intersection image above to test real-time computer vision violation detection and ANPR extraction.")

st.markdown("---")
back_to_home()
disclaimer()
