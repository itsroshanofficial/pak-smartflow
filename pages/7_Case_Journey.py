import streamlit as st
import pandas as pd
from ui import inject_css, hero, pipeline, terminal, disclaimer, CYAN, AMBER, GREEN, RED

st.set_page_config(page_title="Case Journey · Pak-SmartFlow", page_icon="🎬", layout="wide")
inject_css()

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
