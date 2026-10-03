import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from pak_smartflow_engine import pak_smartflow_engine
from db_helper import insert_violation
from ui import (inject_css, hero, kpi, agent_card, style_fig, disclaimer,
                AGENTS, AMBER, CYAN, GREEN, RED, VIOLET)

st.set_page_config(page_title="Pak-SmartFlow · Command Center", page_icon="🚦", layout="wide")
inject_css()

hero(
    "🚦 Pak-SmartFlow Command Center",
    "AI-Powered Multi-Agent Traffic Intelligence, Safety & Compliance Platform",
    [("● LIVE MONITORING", GREEN), ("12 AGENTS", CYAN), ("EXPLAINABLE AI", VIOLET), ("SIMULATION", AMBER)],
)

# ---------- KPI row ----------
rng = np.random.RandomState(7)
k = st.columns(6)
with k[0]: kpi("Violations Today", "1,284", "▲ 8.2% vs yesterday", RED)
with k[1]: kpi("Evidence Verified", "97.2%", "▲ 1.1%", GREEN)
with k[2]: kpi("Challans Issued", "932", "Simulated", AMBER)
with k[3]: kpi("Collection Rate", "68%", "▲ 4% after reminders", GREEN)
with k[4]: kpi("Open Disputes", "37", "14 awaiting review", AMBER)
with k[5]: kpi("Escalations", "11", "Authority queue", RED)

st.write("")
c1, c2 = st.columns([1.6, 1])

with c1:
    hours = list(range(24))
    base = np.array([12,8,6,5,7,15,40,85,120,95,70,65,72,68,64,70,95,130,125,90,60,40,25,16])
    df_h = pd.DataFrame({"Hour": hours, "Violations": base + rng.randint(-6, 7, 24)})
    fig = px.area(df_h, x="Hour", y="Violations", title="Violations by hour (synthetic)")
    fig.update_traces(line_color=AMBER, fillcolor="rgba(245,184,61,.18)")
    st.plotly_chart(style_fig(fig, 300), use_container_width=True)

with c2:
    types = ["Wrong Parking", "Speeding", "Red Light", "Dangerous Driving"]
    fig = go.Figure(go.Pie(labels=types, values=[42, 31, 19, 8], hole=.62,
                           marker=dict(colors=[CYAN, AMBER, RED, VIOLET])))
    fig.update_layout(title="Violation mix")
    st.plotly_chart(style_fig(fig, 300), use_container_width=True)

c3, c4 = st.columns([1, 1.3])
with c3:
    st.markdown("#### 🗺️ Risk Hotspots")
    hot = pd.DataFrame({
        "lat": [31.5204, 31.4504, 33.6844, 33.5651, 24.8607, 31.4187],
        "lon": [74.3587, 73.1350, 73.0479, 73.0169, 67.0011, 73.0790],
        "size": [900, 500, 700, 450, 1100, 380],
    })
    st.map(hot, size="size", color="#F5B83D")

with c4:
    st.markdown("#### ⚡ Live Decision Feed")
    if "feed" not in st.session_state:
        st.session_state.feed = []
    if st.button("⚡ Simulate incoming violation", use_container_width=True):
        viol = random.choice([("Wrong Parking", .3), ("Speeding", .6), ("Red Light", .8), ("Dangerous Driving", 1.0)])
        r = pak_smartflow_engine(
            round(random.uniform(.8, .99), 2), viol[1], round(random.uniform(.2, .9), 2),
            round(random.uniform(.2, .9), 2), round(random.uniform(.1, .8), 2),
            round(random.uniform(.2, .9), 2), round(random.uniform(.2, .9), 2))
        
        plate_no = f"{random.choice(['LEA','ISB','RSP','KHI'])}-{random.randint(1000,9999)}"
        
        # Supabase database mein record insert karna
        insert_violation(
            plate=plate_no,
            violation_type=viol[0],
            risk_score=r["Risk Score"],
            final_score=r["Final Decision Score"],
            action=r["Recommended Action"]
        )

        st.session_state.feed.insert(0, {
            "Plate": plate_no,
            "Violation": viol[0], "Risk": r["Risk Score"],
            "Final Score": r["Final Decision Score"], "Action": r["Recommended Action"]})
    feed = pd.DataFrame(st.session_state.feed[:8]) if st.session_state.feed else pd.DataFrame(
        [{"Plate": "LEA-9871", "Violation": "Red Light", "Risk": .78, "Final Score": .632,
          "Action": "Simulated Enforcement Request / Human Review"}])
    st.dataframe(feed, use_container_width=True, hide_index=True)

# ---------- Agent grid ----------
st.markdown("#### 🤖 The 12-Agent Network")
cols = st.columns(4)
for i, (ic, nm, num, col) in enumerate(AGENTS):
    with cols[i % 4]:
        agent_card(ic, nm, num, col)

# ---------- Quick Navigation for Mobile/Web ----------
st.markdown("---")
st.markdown("#### 🧭 Quick Page Navigation (All Modules)")
nav1, nav2, nav3 = st.columns(3)
with nav1:
    st.page_link("pages/7_Case_Journey.py", label="🎬 Case Journey", icon="🎬")
    st.page_link("pages/8_Emergency_Traffic.py", label="🚑 Emergency Traffic", icon="🚑")
with nav2:
    st.page_link("pages/Compliance_Enforcement.py", label="🛡️ Compliance & Enforcement", icon="🛡️")
    st.page_link("pages/Dispute_Center.py", label="⚖️ Dispute Center", icon="⚖️")
with nav3:
    st.page_link("pages/Alert_System.py", label="🚨 Alert System", icon="🚨")
    st.page_link("pages/2_Historical_Analytics.py", label="📈 Historical Analytics", icon="📈")

st.markdown("#### 🎬 Judges ke liye Special Demos")
a, b = st.columns(2)
with a:
    st.page_link("pages/7_Case_Journey.py", label="▶ Start End-to-End Demo (Detection → Resolution)", icon="🎬")
with b:
    st.page_link("pages/8_Emergency_Traffic.py", label="🚑 Emergency Green Corridor + Signal Optimizer", icon="🚦")

disclaimer()
