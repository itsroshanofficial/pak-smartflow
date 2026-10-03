import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Pak-SmartFlow - Dispute & Appeal Center",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Agent 8: Dispute & Explainability Center")
st.subheader("Transparent AI Decision Log & Citizen Appeal Management")

st.markdown("---")

st.markdown("### 🔍 Lookup Violation for Explainability & Appeal")
search_id = st.text_input("Enter Challan / Vehicle Reference ID", "PSF-2026-9871")

if search_id:
    st.info(f"Displaying explainable AI breakdown for reference: **{search_id}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Model Confidence", "96.4%")
        st.metric("Risk Score Assessed", "0.78 (High)")
        st.metric("Primary Trigger", "Speeding + Lane Violation")
    with col2:
        st.metric("Evidence Status", "Verified by Vision Agent")
        st.metric("Dispute Window", "Active (14 Days Remaining)")
        st.metric("Current Status", "Pending Payment / Unresolved")
        
    st.markdown("---")
    st.markdown("### 📝 Submit Formal Dispute / Appeal")
    
    dispute_reason = st.selectbox(
        "Select Ground for Appeal",
        ["Incorrect Vehicle Number Plate (ANPR Error)", "Medical / Emergency Situation", "Vehicle Sold Prior to Violation Date", "Other Administrative Error"]
    )
    
    citizen_comment = st.text_area("Provide Detailed Explanation / Context", "Please review the attached evidence; speed sensor calibration may have been inaccurate.")
    
    if st.button("📤 Submit Dispute to Authority Review"):
        st.success("✅ Dispute successfully logged and forwarded to Agent 11 for Authority Review Simulation!")
        
        # Log export
        dispute_df = pd.DataFrame([{
            "Reference ID": search_id,
            "Reason": dispute_reason,
            "Comment": citizen_comment,
            "Status": "Under Authority Review"
        }])
        csv = dispute_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Dispute Receipt (CSV)", data=csv, file_name="dispute_receipt.csv", mime="text/csv")
