import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from ui import inject_css, hero, pipeline, terminal, disclaimer, CYAN, AMBER, GREEN, RED, VIOLET

st.set_page_config(page_title="Case Journey · Pak-SmartFlow", page_icon="🎬", layout="wide")
inject_css()

# True Back Button (Browser history back) aur Main Dashboard link sath mein
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
    "🎬 End-to-End Case Journey",
    "Step-by-step walkthrough from violation detection to resolution and compliance.",
    [("SIMULATION", AMBER), ("EXPLAINABLE AI", CYAN)]
)

pipeline(
    ["1. Detection", "2. ANPR & Vehicle", "3. Evidence", "4. Risk Score", "5. Fuzzy Decision", "6. Notice Sent", "7. Resolution"],
    current=4
)

st.markdown("### 🔍 Live Agent Pipeline Execution")
terminal([
    ("ok", "[Agent 1 - Detection] Camera feed captured vehicle frame at 09:42:15."),
    ("ok", "[Agent 2 - ANPR] Plate recognized: LEA-9871 (Confidence: 98.4%)."),
    ("ok", "[Agent 3 - Evidence] Image and timestamp verified against tampering."),
    ("warn", "[Agent 4 - Risk & Context] High traffic congestion zone detected. Risk Score: 0.78."),
    ("ok", "[Agent 6 - Fuzzy Engine] Final Decision Score: 0.632 -> Recommended: Human Review / Notice.")
])

st.markdown("### 📊 Decision Explainability Breakdown")
st.write("Yeh graph batata hai ke multi-agent system ne kis tarah risk score aur weights calculate kiye hain.")

disclaimer()
