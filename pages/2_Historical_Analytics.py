import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from db_helper import get_violations
from ui import inject_css, hero, kpi, style_fig, disclaimer, CYAN, AMBER, GREEN, RED

st.set_page_config(page_title="Historical Analytics · Pak-SmartFlow", page_icon="📈", layout="wide")
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
    "📈 Historical Analytics & Cloud Data",
    "Real-time traffic intelligence and historical violation trends fetched directly from Supabase.",
    [("LIVE DATABASE", GREEN), ("SUPABASE SYNC", CYAN)]
)

# Supabase se real data fetch karna
data = get_violations(limit=100)

if not data or len(data) == 0:
    st.info("⚠️ Database mein abhi koi violations record nahi hain. Command Center par ja kar 'Simulate incoming violation' click karein taake real data save ho jaye!")
else:
    df = pd.DataFrame(data)

    # Summary KPIs real data ke mutabiq
    total_violations = len(df)
    unique_vehicles = df["plate"].nunique() if "plate" in df.columns else 0
    avg_risk = round(df["risk_score"].mean(), 2) if "risk_score" in df.columns and not df["risk_score"].isnull().all() else 0.0

    k1, k2, k3 = st.columns(3)
    with k1:
        kpi("Total Logged Violations", str(total_violations), "From Supabase Cloud", GREEN)
    with k2:
        kpi("Unique Vehicles Tracked", str(unique_vehicles), "Distinct Plates", CYAN)
    with k3:
        kpi("Average Risk Score", str(avg_risk), "Calculated Risk", AMBER)

    st.markdown("---")
    st.markdown("### 📋 Recent Violation Logs (Supabase Live Data)")
    st.dataframe(df, use_container_width=True, hide_index=True)

    if "violation_type" in df.columns and "risk_score" in df.columns:
        st.markdown("### 📊 Risk Score Trends Across Cases")
        fig = px.scatter(df, x="violation_type", y="risk_score", color="violation_type",
                         title="Risk Score Distribution by Violation Type",
                         color_discrete_sequence=[CYAN, AMBER, RED, GREEN])
        st.plotly_chart(style_fig(fig, 300), use_container_width=True)

disclaimer()
