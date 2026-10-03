import streamlit as st
from ui_kit import inject_css, hero, kpi, disclaimer

st.set_page_config(page_title="Pak-SmartFlow", page_icon="🚦", layout="wide")
inject_css()

hero(
    "Pak-SmartFlow Traffic Intelligence",
    "AI-Powered Multi-Agent System from Challan Generation to Compliance Resolution.",
    [("Cloud Connected", "#34D399"), ("Supabase DB", "#38BDF8"), ("Live System", "#F5B83D")]
)

st.subheader("System Overview")
col1, col2, col3 = st.columns(3)
with col1:
    kpi("Active Agents", "12 / 12", "All systems operational", "#34D399")
with col2:
    kpi("Cloud Status", "Connected", "Supabase DB Synced", "#38BDF8")
with col3:
    kpi("Security", "Secured", "Secrets Configured", "#F5B83D")

disclaimer()
