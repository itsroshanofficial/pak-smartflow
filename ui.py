"""Pak-SmartFlow shared UI kit: theme CSS + reusable components."""
import streamlit as st
import plotly.graph_objects as go

AMBER, CYAN, GREEN, RED, VIOLET, SHADE = "#F5B83D", "#38BDF8", "#34D399", "#F87171", "#A78BFA", "rgba(255,255,255,0.08)"

AGENTS = [
    ("📷", "Detection", "Agent 1", CYAN),
    ("🔎", "Vehicle & ANPR", "Agent 2", CYAN),
    ("🧾", "Evidence Verification", "Agent 3", CYAN),
    ("🧭", "Risk & Context", "Agent 4", VIOLET),
    ("🔮", "Predictive Safety", "Agent 5", VIOLET),
    ("🧮", "Fuzzy Decision Engine", "Agent 6", AMBER),
    ("📨", "Action & Notification", "Agent 7", GREEN),
    ("⚖️", "Dispute & Explainability", "Agent 8", GREEN),
    ("🚑", "Emergency Priority", "Agent 9", RED),
    ("🚦", "Traffic Optimization", "Agent 10", CYAN),
    ("🛡️", "Compliance & Enforcement", "Agent 11", AMBER),
    ("💳", "Payment Recovery", "Agent 12", GREEN),
]

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, .stApp { font-family: 'Inter', sans-serif; }
.stApp { background: radial-gradient(900px 500px at 8% -10%, rgba(56,189,248,.14), transparent), radial-gradient(800px 500px at 100% 0%, rgba(245,184,61,.10), transparent), #0D1B2A; }

/* Streamlit elements hide karne ke liye rules */
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }
.stAppDeployButton { display: none; }
[data-testid="stToolbar"] { visibility: hidden; display: none; }
[data-testid="stDecoration"] { visibility: hidden; }

.block-container { padding-top: 1.4rem; max-width: 1280px; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#0f2238,#0a1626); border-right: 1px solid rgba(255,255,255,.06); }

/* Sidebar Navigation ko mazeed bold aur behtar banane ke liye */
[data-testid="stSidebarNav"] span {
    font-weight: 800 !important;
    font-size: 15px !important;
    color: #F5B83D !important;
    letter-spacing: -0.2px;
}
[data-testid="stSidebarNav"] a {
    padding: 6px 10px !important;
    margin-bottom: 4px !important;
    border-radius: 8px !important;
    transition: all 0.2s ease-in-out;
}
[data-testid="stSidebarNav"] a:hover {
    background-color: rgba(245, 184, 61, 0.18) !important;
    transform: translateX(3px);
}

.hero { padding: 26px 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,.08); background: linear-gradient(135deg, rgba(20,38,59,.95), rgba(13,27,42,.9)); position: relative; overflow: hidden; margin-bottom: 18px; }
.hero:before { content:""; position:absolute; top:-120px; right:-80px; width:380px; height:380px; background: radial-gradient(circle, rgba(245,184,61,.22), transparent 65%); }
.hero h1 { margin:0; font-size:2rem; font-weight:800; letter-spacing:-.5px; position:relative; }
.hero p { margin:.4rem 0 .7rem; color:#9fb3c8; position:relative; }
.tag { display:inline-block; padding:3px 11px; border-radius:999px; font-size:.72rem; font-weight:600; border:1px solid; margin:0 6px 4px 0; position:relative; }
.kpi { padding:16px 18px; border-radius:16px; background:rgba(20,38,59,.75); border:1px solid rgba(255,255,255,.07); transition:transform .2s, border-color .2s; }
.kpi:hover { transform:translateY(-3px); border-color:rgba(245,184,61,.5); }
.kpi .l { color:#8ea5bd; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; }
.kpi .v { font-size:1.7rem; font-weight:800; margin-top:2px; }
.kpi .d { font-size:.78rem; margin-top:2px; }
.agent { padding:13px 14px; border-radius:14px; background:rgba(20,38,59,.6); border:1px solid rgba(255,255,255,.06); transition:all .2s; margin-bottom:10px; }
.agent:hover { border-color:var(--c); box-shadow:0 0 24px -8px var(--c); transform:translateY(-2px); }
.agent .n { font-size:.68rem; color:#8ea5bd; }
.agent .t { font-weight:700; margin:2px 0; font-size:.9rem; }
.agent .s { font-size:.72rem; color:#34D399; }
.pipe { display:flex; flex-wrap:wrap; gap:8px; margin:6px 0 14px; }
.pstep { padding:6px 12px; border-radius:999px; font-size:.76rem; font-weight:600; border:1px solid rgba(255,255,255,.1); color:#6f869d; background:rgba(255,255,255,.02); }
.pstep.done { color:#34D399; border-color:rgba(52,211,153,.4); background:rgba(52,211,153,.08); }
.pstep.now { color:#0D1B2A; background:#F5B83D; border-color:#F5B83D; box-shadow:0 0 18px rgba(245,184,61,.5); }
.pstep.bad { color:#F87171; border-color:rgba(248,113,113,.45); background:rgba(248,113,113,.08); }
.panel { padding:18px 20px; border-radius:16px; background:rgba(20,38,59,.7); border:1px solid rgba(255,255,255,.07); margin-bottom:12px; }
.panel h3 { margin:0 0 6px; font-size:1.15rem; }
.panel p { margin:0; color:#b5c6d8; }
.term { font-family:ui-monospace,Menlo,Consolas,monospace; font-size:.78rem; background:#08121e; border:1px solid rgba(255,255,255,.07); border-radius:12px; padding:12px 14px; color:#9ad1ff; max-height:280px; overflow:auto; line-height:1.65; }
.term .ok { color:#34D399; } .term .warn { color:#F5B83D; } .term .err { color:#F87171; }
.sim { display:inline-block; padding:2px 9px; border-radius:6px; font-size:.68rem; font-weight:700; letter-spacing:.06em; color:#F5B83D; border:1px dashed rgba(245,184,61,.6); }
</style>
"""

def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown(
            "<div style='padding:6px 4px 10px'><div style='font-size:1.35rem;font-weight:800'>"
            "🚦 Pak-<span style=\"color:#F5B83D\">SmartFlow</span></div>"
            "<div style='color:#8ea5bd;font-size:.75rem'>From Challan Generation to Compliance Resolution</div>"
            "<div style='margin-top:8px'><span class='sim'>SIMULATION · SYNTHETIC DATA</span></div></div>",
            unsafe_allow_html=True,
        )

def hero(title, subtitle, tags=()):
    chips = "".join(
        f"<span class='tag' style='color:{c};border-color:{c}55;background:{c}14'>{t}</span>"
        for t, c in tags
    )
    st.markdown(
        f"<div class='hero'><h1>{title}</h1><p>{subtitle}</p>{chips}</div>",
        unsafe_allow_html=True,
    )

def kpi(label, value, delta="", color=GREEN):
    st.markdown(
        f"<div class='kpi'><div class='l'>{label}</div><div class='v'>{value}</div>"
        f"<div class='d' style='color:{color}'>{delta}</div></div>",
        unsafe_allow_html=True,
    )

def agent_card(icon, name, num, color, status="Online"):
    st.markdown(
        f"<div class='agent' style='--c:{color}'><div class='n'>{num}</div>"
        f"<div class='t'>{icon} {name}</div><div class='s'>● {status}</div></div>",
        unsafe_allow_html=True,
    )

def pipeline(labels, current, bad=()):
    parts = []
    for i, lb in enumerate(labels):
        cls = "bad" if i in bad and i < current else "done" if i < current else "now" if i == current else ""
        parts.append(f"<span class='pstep {cls}'>{lb}</span>")
    st.markdown("<div class='pipe'>" + "".join(parts) + "</div>", unsafe_allow_html=True)

def terminal(lines):
    body = "<br>".join(f"<span class='{c}'>{t}</span>" for c, t in lines) or "<span>waiting…</span>"
    st.markdown(f"<div class='term'>{body}</div>", unsafe_allow_html=True)

def style_fig(fig, height=300):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d6e4", family="Inter"),
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(orientation="h", y=-0.15),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,.06)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,.06)")
    return fig

def gauge(value, title, low=0.3, high=0.6, height=230, invert=False):
    good, bad = (GREEN, RED) if not invert else (RED, GREEN)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(value, 3),
        title={"text": title, "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, 1]},
            "bar": {"color": "#E6EDF5", "thickness": 0.22},
            "bgcolor": "rgba(0,0,0,0)",
            "steps": [
                {"range": [0, low], "color": f"{good}55"},
                {"range": [low, high], "color": f"{AMBER}55"},
                {"range": [high, 1], "color": f"{bad}55"},
            ],
        },
    ))
    return style_fig(fig, height)

def disclaimer():
    st.markdown(
        "<div style='margin-top:14px;color:#8ea5bd;font-size:.78rem'>⚠️ Prototype / simulation. "
        "Koi bhi enforcement action sirf authorized authority ke review ke baad ho sakta hai.</div>",
        unsafe_allow_html=True,
    )
