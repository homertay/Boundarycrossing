"""
MBX Boundary Crossing Diagnostic — Enhanced Version
Master in Boundary-Crossing Learning and Leadership | IAL/SUSS

Features:
  • Polished UI with custom CSS (academic-professional tone)
  • 4-dimension, 20-question diagnostic (Akkerman & Bakker framework)
  • Step-by-step question flow (one dimension per screen)
  • Radar chart + dimension score cards with developmental feedback
  • HTML report download (printable / save-as-PDF)
  • Optional submit-to-class (shared in-memory store via st.cache_resource)
  • Facilitator dashboard: aggregate radar, participant table, CSV export
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Boundary Crossing Diagnostic | MBX",
    page_icon="🔀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

FACILITATOR_PASSWORD = "mbx2026"   # ← change before class


# ─────────────────────────────────────────────────────────────────────────────
#  SHARED CLASS STORE
#  st.cache_resource persists for the lifetime of the server process.
#  Everyone on the same Streamlit instance shares this list — ideal for a
#  classroom session. It resets only if the app restarts.
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_class_store():
    return []


# ─────────────────────────────────────────────────────────────────────────────
#  DIAGNOSTIC CONTENT
# ─────────────────────────────────────────────────────────────────────────────
DIMENSIONS = [
    {
        "key": "awareness",
        "name": "Boundary Awareness",
        "color": "#3B82F6",
        "icon": "🔍",
        "tagline": "Noticing and naming the limits of your practice",
        "questions": [
            "I can identify when I am working across different professional or disciplinary communities.",
            "I notice when my assumptions differ from those of colleagues in other teams or organisations.",
            "I can articulate what makes cross-boundary collaboration genuinely difficult.",
            "I recognise when a boundary is limiting progress on a shared goal.",
            "I am aware of how my 'home practice' shapes my perspective when I work in unfamiliar territory.",
        ],
        "feedback": [
            "You may benefit from developing greater sensitivity to the invisible lines that shape collaboration. Try reflecting on moments of friction or surprise — these are often boundary signals.",
            "You notice boundaries in familiar contexts. The next step is applying this awareness more consistently in unfamiliar or complex multi-stakeholder situations.",
            "You have a well-developed capacity to name and navigate invisible boundaries. Consider helping others develop this awareness as part of your leadership practice.",
        ],
    },
    {
        "key": "coordination",
        "name": "Coordination",
        "color": "#10B981",
        "icon": "🤝",
        "tagline": "Building bridges, routines, and shared language",
        "questions": [
            "I actively create shared language or frameworks when working with people from different backgrounds.",
            "I help establish common ground when groups with different goals need to collaborate.",
            "I design artefacts or processes that allow people to work productively across organisational lines.",
            "I am effective at managing handoffs and transitions between different teams or phases.",
            "I build relationships intentionally to navigate institutional or cultural boundaries.",
        ],
        "feedback": [
            "Consider how you might build more deliberate bridging structures. Boundary objects — shared artefacts, templates, frameworks — can help create common ground.",
            "You coordinate well in familiar settings. Try experimenting with new bridging approaches in more complex or unfamiliar multi-stakeholder environments.",
            "You are skilled at creating the scaffolding that makes cross-boundary work viable. Look for opportunities to teach and share these practices.",
        ],
    },
    {
        "key": "reflection",
        "name": "Reflective Capacity",
        "color": "#F59E0B",
        "icon": "🪞",
        "tagline": "Learning about yourself through encounters with difference",
        "questions": [
            "Encountering different professional perspectives causes me to question my own assumptions.",
            "I actively seek out viewpoints that challenge my existing mental models.",
            "I use cross-boundary encounters as opportunities to deepen my self-understanding.",
            "I can articulate how working with others has changed how I see my own field.",
            "I regularly create space to reflect on what I have learned from cross-boundary experiences.",
        ],
        "feedback": [
            "Deepening your reflective practice could help you extract more learning from boundary encounters. Try journalling about moments of surprise or discomfort in collaborative work.",
            "You reflect when prompted. Building regular reflection habits — even briefly — could significantly amplify your learning from boundary encounters.",
            "You extract significant learning from your cross-boundary experiences through sustained reflection. Your perspective-taking capacity is a key leadership strength.",
        ],
    },
    {
        "key": "transformation",
        "name": "Transformative Practice",
        "color": "#8B5CF6",
        "icon": "✨",
        "tagline": "Generating new knowledge and practices through crossing",
        "questions": [
            "I have developed new approaches to my work by combining insights from different fields.",
            "I contribute to creating shared solutions that would not emerge within a single discipline.",
            "I help others see their work differently by introducing perspectives from outside their domain.",
            "I translate ideas from one context in ways that create genuine value in another.",
            "I am involved in shaping new practices or structures that bridge previously separate domains.",
        ],
        "feedback": [
            "Your boundary crossings may not yet be generating transformative outputs. Reflect on what new practices could emerge from your current cross-boundary encounters.",
            "You occasionally generate new insights from crossing. Look for deliberate opportunities to synthesise across domains and share what you create with both communities.",
            "You are not just crossing boundaries — you are transforming practices on both sides. This is the highest expression of boundary-crossing leadership.",
        ],
    },
]

LIKERT = ["Rarely", "Sometimes", "Often", "Usually", "Almost Always"]


# ─────────────────────────────────────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────────────────────────────────────
def compute_scores(responses: dict) -> dict:
    scores = {}
    for dim in DIMENSIONS:
        keys = [f"{dim['key']}_{i}" for i in range(5)]
        vals = [responses.get(k, 3) for k in keys]
        scores[dim["key"]] = round(sum(vals) / len(vals), 2)
    return scores


def score_tier(s: float):
    """Return (label, hex_color, feedback_index) for a score 1-5."""
    if s < 2.5:
        return "Emerging", "#F97316", 0
    if s < 3.5:
        return "Developing", "#3B82F6", 1
    if s < 4.25:
        return "Proficient", "#10B981", 2
    return "Advanced", "#8B5CF6", 2


def make_radar(all_scores: list, labels: list = None, title: str = "Boundary Crossing Profile"):
    dim_names = [d["name"] for d in DIMENSIONS]
    dim_keys = [d["key"] for d in DIMENSIONS]
    palette = ["#2563EB", "#F59E0B", "#10B981", "#8B5CF6", "#EF4444"]

    fig = go.Figure()
    if not isinstance(all_scores, list):
        all_scores = [all_scores]
    if labels is None:
        labels = [f"Profile {i + 1}" for i in range(len(all_scores))]

    for i, scores in enumerate(all_scores):
        vals = [scores[k] for k in dim_keys] + [scores[dim_keys[0]]]
        theta = dim_names + [dim_names[0]]
        c = palette[i % len(palette)]
        r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
        fig.add_trace(
            go.Scatterpolar(
                r=vals,
                theta=theta,
                fill="toself",
                fillcolor=f"rgba({r},{g},{b},0.12)",
                line=dict(color=c, width=2.5),
                name=labels[i],
            )
        )

    fig.update_layout(
        polar=dict(
            bgcolor="rgba(248,250,252,0.8)",
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                tickfont=dict(size=10, color="#94A3B8"),
                gridcolor="rgba(148,163,184,0.3)",
                linecolor="rgba(148,163,184,0.3)",
            ),
            angularaxis=dict(
                gridcolor="rgba(148,163,184,0.2)",
                tickfont=dict(size=12, color="#334155"),
            ),
        ),
        showlegend=len(all_scores) > 1,
        legend=dict(font=dict(size=11)),
        title=dict(
            text=title,
            font=dict(size=15, color="#1E293B", family="Georgia, serif"),
            x=0.5,
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=440,
        margin=dict(t=70, b=20, l=30, r=30),
    )
    return fig


def html_report(name: str, scores: dict, class_code: str = "") -> str:
    now = datetime.now().strftime("%d %B %Y")
    rows = ""
    for dim in DIMENSIONS:
        s = scores[dim["key"]]
        label, color, tier_idx = score_tier(s)
        pct = (s / 5) * 100
        feedback_text = dim["feedback"][tier_idx]
        rows += f"""
        <div style="background:white;border-radius:12px;padding:1.3rem 1.5rem;margin-bottom:1rem;
                    border-left:5px solid {dim['color']};box-shadow:0 2px 8px rgba(0,0,0,0.07)">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
            <span style="font-weight:700;font-size:1rem;color:#1E293B">{dim['icon']} {dim['name']}</span>
            <span style="background:{color};color:white;padding:3px 12px;border-radius:999px;
                         font-size:0.76rem;font-weight:700;letter-spacing:0.5px">{label.upper()}</span>
          </div>
          <div style="font-size:1.7rem;font-weight:800;color:#1E293B;margin-bottom:6px;font-family:Georgia,serif">
            {s:.1f}<span style="font-size:1rem;font-weight:400;color:#94A3B8"> / 5.0</span></div>
          <div style="background:#E2E8F0;border-radius:999px;height:8px;margin-bottom:10px">
            <div style="background:{dim['color']};width:{pct:.0f}%;height:8px;border-radius:999px"></div>
          </div>
          <p style="margin:0;font-size:0.88rem;color:#64748B;line-height:1.7">{feedback_text}</p>
        </div>"""

    meta = f"{name}"
    if class_code:
        meta += f" &nbsp;·&nbsp; {class_code}"
    meta += f" &nbsp;·&nbsp; {now}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boundary Crossing Profile — {name}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;700&family=DM+Sans:wght@400;500;600&display=swap');
  body {{
    font-family: 'DM Sans', sans-serif;
    max-width: 700px; margin: 40px auto; padding: 0 24px;
    color: #1E293B; background: #F8FAFC;
  }}
  .header {{
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #2563EB 100%);
    border-radius: 16px; padding: 2.5rem 2rem; color: white; margin-bottom: 1.5rem;
  }}
  .header .label {{
    font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase;
    opacity: 0.6; margin-bottom: 0.6rem;
  }}
  .header h1 {{
    margin: 0; font-size: 1.8rem; font-family: 'Lora', Georgia, serif; font-weight: 700;
  }}
  .header .meta {{ margin: 8px 0 0; opacity: 0.8; font-size: 0.9rem; }}
  .reflection {{
    background: #EFF6FF; border-left: 4px solid #2563EB; border-radius: 8px;
    padding: 1.2rem 1.4rem; margin: 1.5rem 0;
  }}
  .reflection h3 {{ margin: 0 0 0.5rem; color: #1D4ED8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }}
  .reflection p {{ margin: 0; color: #475569; font-size: 0.9rem; line-height: 1.7; font-style: italic; }}
  .footer {{
    text-align: center; font-size: 0.78rem; color: #CBD5E1; margin-top: 2rem; padding-top: 1rem;
    border-top: 1px solid #E2E8F0;
  }}
</style>
</head>
<body>
  <div class="header">
    <div class="label">MBX · Master in Boundary-Crossing Learning and Leadership · IAL/SUSS</div>
    <h1>Boundary Crossing Profile</h1>
    <div class="meta">{meta}</div>
  </div>
  {rows}
  <div class="reflection">
    <h3>💭 Reflection Prompt</h3>
    <p>Looking at your profile: Where does your highest score align with your current role?
       Where is the gap between your boundary-crossing capacity and what your context demands?
       What is one specific boundary you want to cross more effectively in the next three months?</p>
  </div>
  <div class="footer">MBX Boundary Crossing Diagnostic · IAL/SUSS · {now}</div>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.main { background: #F8FAFC; }

.block-container {
    padding-top: 1.5rem !important;
    max-width: 700px !important;
}

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 60%, #2563EB 100%);
    border-radius: 18px;
    padding: 2.8rem 2.2rem;
    color: white;
    margin-bottom: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%; right: -20%;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-label {
    font-size: 0.62rem; letter-spacing: 3px; text-transform: uppercase;
    opacity: 0.6; margin-bottom: 0.8rem;
}
.hero h1 {
    font-family: 'Lora', Georgia, serif;
    font-size: 2rem; font-weight: 700; margin: 0;
    letter-spacing: -0.5px; line-height: 1.2;
}
.hero p {
    font-size: 0.95rem; opacity: 0.8; margin: 0.9rem 0 0;
    line-height: 1.65; max-width: 500px; margin-left: auto; margin-right: auto;
}

/* Info card */
.info-card {
    background: white; border-radius: 14px; padding: 1.4rem 1.6rem;
    margin-bottom: 1rem; box-shadow: 0 1px 6px rgba(15,23,42,0.07);
    border: 1px solid rgba(226,232,240,0.8);
}

/* Progress bar */
.prog-wrap { margin-bottom: 1.2rem; }
.prog-label {
    display: flex; justify-content: space-between;
    font-size: 0.78rem; color: #64748B; margin-bottom: 5px;
}
.prog-bg {
    background: #E2E8F0; border-radius: 999px; height: 6px;
}
.prog-fill {
    height: 6px; border-radius: 999px;
    background: linear-gradient(90deg, #1E40AF, #3B82F6);
    transition: width 0.4s ease;
}

/* Dimension header */
.dim-header {
    background: white; border-radius: 14px; padding: 1.2rem 1.5rem;
    margin-bottom: 1.2rem; box-shadow: 0 1px 5px rgba(15,23,42,0.07);
    border: 1px solid rgba(226,232,240,0.8);
    display: flex; align-items: center; gap: 1rem;
}
.dim-icon { font-size: 2rem; }
.dim-name { font-weight: 700; font-size: 1.05rem; color: #1E293B; }
.dim-tagline { font-size: 0.82rem; color: #64748B; margin-top: 2px; }

/* Question card */
.q-card {
    background: white; border-radius: 12px; padding: 1.1rem 1.4rem;
    margin-bottom: 0.75rem; box-shadow: 0 1px 4px rgba(15,23,42,0.06);
    border: 1px solid rgba(226,232,240,0.7);
}
.q-text {
    font-size: 0.93rem; color: #1E293B; line-height: 1.6;
    font-weight: 500; margin-bottom: 0.75rem;
}

/* Result score card */
.r-card {
    background: white; border-radius: 14px; padding: 1.3rem 1.5rem;
    margin-bottom: 0.85rem; box-shadow: 0 2px 8px rgba(15,23,42,0.07);
    border: 1px solid rgba(226,232,240,0.8);
}
.r-header {
    display: flex; justify-content: space-between; align-items: flex-start;
    margin-bottom: 0.6rem;
}
.r-name { font-weight: 700; font-size: 0.97rem; color: #1E293B; }
.r-tagline { font-size: 0.78rem; color: #94A3B8; margin-top: 3px; }
.r-badge {
    color: white; padding: 3px 12px; border-radius: 999px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px;
    white-space: nowrap;
}
.r-score {
    font-family: 'Lora', Georgia, serif;
    font-size: 2rem; font-weight: 700; color: #1E293B;
    margin-bottom: 6px; line-height: 1;
}
.r-score span { font-family: 'DM Sans', sans-serif; font-size: 1rem; font-weight: 400; color: #94A3B8; }
.r-bar-bg { background: #E2E8F0; border-radius: 999px; height: 7px; margin-bottom: 0.85rem; }
.r-bar-fill { height: 7px; border-radius: 999px; }
.r-feedback { font-size: 0.88rem; color: #475569; line-height: 1.7; margin: 0; }

/* Reflection box */
.reflect-box {
    background: #EFF6FF; border-left: 4px solid #2563EB; border-radius: 10px;
    padding: 1.2rem 1.4rem; margin: 1.25rem 0;
}
.reflect-title { font-weight: 700; color: #1D4ED8; font-size: 0.85rem; margin-bottom: 0.5rem; }
.reflect-text { font-size: 0.9rem; color: #475569; line-height: 1.7; margin: 0; font-style: italic; }

/* Confirm box */
.confirm-box {
    background: linear-gradient(135deg, #064E3B, #059669);
    border-radius: 14px; padding: 1.5rem 2rem;
    color: white; text-align: center; margin: 1rem 0;
}
.confirm-box h3 { margin: 0 0 0.4rem; font-size: 1.1rem; }
.confirm-box p { margin: 0; opacity: 0.85; font-size: 0.88rem; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #1E3A8A, #2563EB) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 0.65rem 1.6rem !important;
    font-weight: 600 !important; font-size: 0.95rem !important;
    transition: all 0.2s !important; width: 100% !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.1px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35) !important;
}

/* Radio styling */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] {
    flex-direction: row !important; flex-wrap: wrap !important; gap: 0.4rem !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background: #F1F5F9; border-radius: 8px; padding: 0.35rem 0.7rem;
    font-size: 0.82rem !important; color: #475569 !important;
    border: 1.5px solid transparent; transition: all 0.15s; cursor: pointer;
}
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background: #EFF6FF; border-color: #2563EB; color: #1D4ED8 !important; font-weight: 600;
}

/* Input fields */
.stTextInput > div > div > input {
    border-radius: 10px !important; border: 1.5px solid #E2E8F0 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important; background: white !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2563EB !important; box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0F172A !important;
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: rgba(255,255,255,0.1) !important;
    border-color: rgba(255,255,255,0.2) !important;
    color: white !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────────────────────────
def init():
    defaults = {
        "page": "welcome",      # welcome | diagnostic | results
        "step": 0,              # 0-3: which dimension we're on
        "responses": {},        # {dim_key_i: int}
        "name": "",
        "class_code": "",
        "scores": None,
        "submitted": False,
        "fac_mode": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR — FACILITATOR LOGIN
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔒 Facilitator Access")
    fac_pw = st.text_input("Password", type="password", key="fac_pw_input", label_visibility="collapsed")
    if st.button("Enter Facilitator View", key="fac_login"):
        if fac_pw == FACILITATOR_PASSWORD:
            st.session_state.fac_mode = True
            st.rerun()
        else:
            st.error("Incorrect password")
    if st.session_state.fac_mode:
        st.success("✅ Facilitator mode active")
        if st.button("Exit Facilitator View"):
            st.session_state.fac_mode = False
            st.rerun()
        st.markdown("---")
        store = get_class_store()
        if store and st.button("🗑 Clear All Results"):
            store.clear()
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
#  FACILITATOR DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.fac_mode:
    store = get_class_store()

    st.markdown(
        """
    <div class="hero" style="text-align:left;padding:1.8rem 2rem">
      <div class="hero-label">Facilitator Dashboard</div>
      <h1 style="font-size:1.6rem">🎓 Class Results</h1>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if not store:
        st.info("📭 No submissions yet. Share the app with participants and ask them to submit to class.")
    else:
        st.metric("Participants submitted", len(store))
        st.markdown("---")

        dim_keys = [d["key"] for d in DIMENSIONS]
        all_dicts = [r["scores"] for r in store]

        # Aggregate average
        avg = {k: round(sum(r[k] for r in all_dicts) / len(all_dicts), 2) for k in dim_keys}

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                make_radar([avg], ["Class Average"], "Class Average"),
                use_container_width=True,
            )
        with col2:
            labels = [r["name"].split()[0] for r in store]  # first name only for chart
            st.plotly_chart(
                make_radar(all_dicts, labels, "All Participants"),
                use_container_width=True,
            )

        # Results table
        st.markdown("#### Individual Scores")
        rows = []
        for r in store:
            row = {"Name": r["name"], "Time": r["timestamp"]}
            for d in DIMENSIONS:
                row[d["name"]] = r["scores"][d["key"]]
            row["Class Code"] = r.get("class_code", "—")
            rows.append(row)
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # CSV download
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download Results CSV",
            data=csv,
            file_name=f"mbx_results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

        # Class discussion starters
        st.markdown("---")
        st.markdown("#### 💬 Discussion Prompts for Debrief")
        
        # Find highest & lowest average dim
        sorted_dims = sorted(dim_keys, key=lambda k: avg[k])
        lowest_dim = next(d for d in DIMENSIONS if d["key"] == sorted_dims[0])
        highest_dim = next(d for d in DIMENSIONS if d["key"] == sorted_dims[-1])
        
        st.markdown(
            f"""
        <div style="background:#F0FDF4;border-left:4px solid #10B981;border-radius:10px;
                    padding:1rem 1.2rem;margin-bottom:0.75rem">
          <strong>Collective strength: {highest_dim['icon']} {highest_dim['name']} 
          ({avg[highest_dim['key']]:.1f}/5)</strong><br>
          <span style="font-size:0.9rem;color:#475569">What conditions in your organisations 
          have made this your strongest collective capacity?</span>
        </div>
        <div style="background:#FFF7ED;border-left:4px solid #F59E0B;border-radius:10px;
                    padding:1rem 1.2rem;margin-bottom:0.75rem">
          <strong>Shared growth edge: {lowest_dim['icon']} {lowest_dim['name']} 
          ({avg[lowest_dim['key']]:.1f}/5)</strong><br>
          <span style="font-size:0.9rem;color:#475569">What structural or cultural factors 
          might be limiting this across your different contexts?</span>
        </div>
        <div style="background:#EFF6FF;border-left:4px solid #2563EB;border-radius:10px;
                    padding:1rem 1.2rem">
          <strong>Individual variation</strong><br>
          <span style="font-size:0.9rem;color:#475569">Whose profile surprised them the most? 
          What does the spread in the class tell us about our different practice contexts?</span>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.stop()


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: WELCOME
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "welcome":
    st.markdown(
        """
    <div class="hero">
      <div class="hero-label">MBX · IAL/SUSS</div>
      <div style="font-size:2.8rem;margin-bottom:0.6rem">🔀</div>
      <h1>Boundary Crossing<br>Diagnostic</h1>
      <p>A self-assessment tool for the MBX community — understand your current 
      boundary-crossing capabilities across four dimensions of practice.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class="info-card">
      <p style="margin:0;color:#475569;line-height:1.75;font-size:0.94rem">
        This diagnostic takes about <strong>8–10 minutes</strong>. You will respond to 
        <strong>20 statements</strong> across four dimensions drawn from boundary-crossing 
        theory (Akkerman &amp; Bakker), then receive a personalised radar profile with 
        developmental feedback.<br><br>
        There are no right or wrong answers — respond based on your 
        <em>typical experience</em>, not an ideal self.
      </p>
    </div>
    <div style="display:flex;gap:0.75rem;margin-bottom:1.25rem;flex-wrap:wrap">
      <div style="background:white;border-radius:10px;padding:0.75rem 1rem;flex:1;min-width:130px;
                  box-shadow:0 1px 4px rgba(0,0,0,0.07);text-align:center">
        <div style="font-size:1.4rem;margin-bottom:3px">🔍</div>
        <div style="font-size:0.78rem;font-weight:600;color:#1E293B">Boundary<br>Awareness</div>
      </div>
      <div style="background:white;border-radius:10px;padding:0.75rem 1rem;flex:1;min-width:130px;
                  box-shadow:0 1px 4px rgba(0,0,0,0.07);text-align:center">
        <div style="font-size:1.4rem;margin-bottom:3px">🤝</div>
        <div style="font-size:0.78rem;font-weight:600;color:#1E293B">Coordination</div>
      </div>
      <div style="background:white;border-radius:10px;padding:0.75rem 1rem;flex:1;min-width:130px;
                  box-shadow:0 1px 4px rgba(0,0,0,0.07);text-align:center">
        <div style="font-size:1.4rem;margin-bottom:3px">🪞</div>
        <div style="font-size:0.78rem;font-weight:600;color:#1E293B">Reflective<br>Capacity</div>
      </div>
      <div style="background:white;border-radius:10px;padding:0.75rem 1rem;flex:1;min-width:130px;
                  box-shadow:0 1px 4px rgba(0,0,0,0.07);text-align:center">
        <div style="font-size:1.4rem;margin-bottom:3px">✨</div>
        <div style="font-size:0.78rem;font-weight:600;color:#1E293B">Transformative<br>Practice</div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    name_val = st.text_input(
        "Your name",
        value=st.session_state.name,
        placeholder="e.g. Wei Lin",
        label_visibility="visible",
    )
    code_val = st.text_input(
        "Class code (provided by your facilitator)",
        value=st.session_state.class_code,
        placeholder="e.g. MBX-APR2026",
        label_visibility="visible",
    )

    if st.button("Begin Diagnostic →"):
        if not name_val.strip():
            st.warning("Please enter your name to continue.")
        else:
            st.session_state.name = name_val.strip()
            st.session_state.class_code = code_val.strip()
            st.session_state.page = "diagnostic"
            st.session_state.step = 0
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: DIAGNOSTIC
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "diagnostic":
    step = st.session_state.step
    dim = DIMENSIONS[step]
    progress_pct = step / len(DIMENSIONS)

    # Progress bar
    st.markdown(
        f"""
    <div class="prog-wrap">
      <div class="prog-label">
        <span>Section {step + 1} of {len(DIMENSIONS)} — {dim['name']}</span>
        <span>{int(progress_pct * 100)}% complete</span>
      </div>
      <div class="prog-bg">
        <div class="prog-fill" style="width:{progress_pct * 100:.0f}%"></div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Dimension header
    st.markdown(
        f"""
    <div class="dim-header" style="border-left:5px solid {dim['color']}">
      <div class="dim-icon">{dim['icon']}</div>
      <div>
        <div class="dim-name">{dim['name']}</div>
        <div class="dim-tagline">{dim['tagline']}</div>
      </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='font-size:0.82rem;color:#94A3B8;margin-bottom:0.75rem'>"
        "Rate each statement: 1 = Rarely · 5 = Almost Always</p>",
        unsafe_allow_html=True,
    )

    # Questions
    all_answered = True
    for i, question in enumerate(dim["questions"]):
        key = f"{dim['key']}_{i}"
        current = st.session_state.responses.get(key, None)

        with st.container():
            st.markdown(
                f'<div class="q-card"><p class="q-text">{i + 1}. {question}</p></div>',
                unsafe_allow_html=True,
            )
            response = st.radio(
                label=f"q_{key}",
                options=list(range(1, 6)),
                format_func=lambda x: f"{x} — {LIKERT[x - 1]}",
                horizontal=True,
                index=current - 1 if current is not None else None,
                key=f"radio_{key}",
            )
            if response is None:
                all_answered = False
            else:
                st.session_state.responses[key] = response

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Navigation
    is_last = step == len(DIMENSIONS) - 1
    col1, col2 = st.columns([1, 2])
    with col1:
        if step > 0:
            if st.button("← Back"):
                st.session_state.step -= 1
                st.rerun()
    with col2:
        next_label = (
            "View My Results →"
            if is_last
            else f"Next: {DIMENSIONS[step + 1]['name']} →"
        )
        if st.button(next_label):
            if not all_answered:
                st.warning("Please respond to all statements before continuing.")
            elif is_last:
                st.session_state.scores = compute_scores(st.session_state.responses)
                st.session_state.page = "results"
                st.rerun()
            else:
                st.session_state.step += 1
                st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
#  PAGE: RESULTS
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "results":
    scores = st.session_state.scores
    name = st.session_state.name

    st.markdown(
        f"""
    <div class="hero" style="padding:2rem;text-align:left">
      <div class="hero-label">Your Profile · MBX</div>
      <h1 style="font-size:1.5rem">Boundary Crossing Profile</h1>
      <p style="margin:6px 0 0;font-size:0.9rem">{name}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Radar chart
    st.plotly_chart(make_radar([scores], [name]), use_container_width=True)

    # Score cards
    st.markdown(
        "<h3 style='font-family:Lora,Georgia,serif;color:#1E293B;margin-bottom:0.75rem'>"
        "Dimension Scores</h3>",
        unsafe_allow_html=True,
    )

    for dim in DIMENSIONS:
        s = scores[dim["key"]]
        label, color, tier_idx = score_tier(s)
        pct = (s / 5) * 100
        feedback_text = dim["feedback"][tier_idx]

        st.markdown(
            f"""
        <div class="r-card" style="border-left:5px solid {dim['color']}">
          <div class="r-header">
            <div>
              <div class="r-name">{dim['icon']} {dim['name']}</div>
              <div class="r-tagline">{dim['tagline']}</div>
            </div>
            <span class="r-badge" style="background:{color}">{label.upper()}</span>
          </div>
          <div class="r-score">{s:.1f}<span> / 5.0</span></div>
          <div class="r-bar-bg">
            <div class="r-bar-fill" style="background:{dim['color']};width:{pct:.0f}%"></div>
          </div>
          <p class="r-feedback">{feedback_text}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Reflection prompt
    st.markdown(
        """
    <div class="reflect-box">
      <div class="reflect-title">💭 Reflection Prompt</div>
      <p class="reflect-text">
        Looking at your profile: Where does your highest score align with your current role?
        Where is the gap between your boundary-crossing capacity and what your context demands?
        What is one specific boundary you want to cross more effectively in the next three months?
      </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Download report
    report = html_report(name, scores, st.session_state.class_code)
    st.download_button(
        "📄 Download My Report (open in browser → Print → Save as PDF)",
        data=report,
        file_name=f"BC_Profile_{name.replace(' ', '_')}.html",
        mime="text/html",
        use_container_width=True,
    )

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # Submit to class
    if not st.session_state.submitted:
        st.markdown(
            """
        <div class="info-card">
          <div style="font-weight:700;color:#1E293B;margin-bottom:0.4rem">📤 Submit to Class Dashboard</div>
          <p style="margin:0;font-size:0.87rem;color:#475569;line-height:1.65">
            Share your scores anonymously with your facilitator's class dashboard. 
            Only your name and dimension scores are submitted — your individual question 
            responses remain private.
          </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        if st.button("✅ Submit to Class"):
            store = get_class_store()
            store.append(
                {
                    "name": name,
                    "class_code": st.session_state.class_code,
                    "scores": scores,
                    "timestamp": datetime.now().strftime("%H:%M"),
                }
            )
            st.session_state.submitted = True
            st.rerun()
    else:
        st.markdown(
            """
        <div class="confirm-box">
          <h3>✅ Submitted to Class Dashboard</h3>
          <p>Your facilitator can now see your profile in the class overview.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    if st.button("🔄 Retake Diagnostic"):
        for k in ["page", "step", "responses", "scores", "submitted"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()
