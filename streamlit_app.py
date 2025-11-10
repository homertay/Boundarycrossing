import random
import streamlit as st
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG + LIGHT CSS
# ============================================================
st.set_page_config(page_title="The Boundary Compass — Singapore Manager Edition",
                   page_icon="🧭", layout="centered")

def apply_css():
    st.markdown("""
    <style>
      .stApp { background: linear-gradient(180deg,#F3F8FC 0%,#FFFFFF 60%); }
      .block-container { max-width: 920px; padding-top: 2rem; padding-bottom: 3rem; }
      details { border-radius: 8px; background: #fff; border: 1px solid #e6e6e6; }
      .stRadio > div { gap: .75rem; }
      .stRadio label {
        background: #ffffff; border: 1px solid #e5e5e5; border-radius: 8px;
        padding: 0.9rem 1rem; width: 100%; transition: background .2s ease;
      }
      .stRadio label:hover { background: #f7fafc; }
      #MainMenu, header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

TITLE = "🧭 The Boundary Compass — Singapore Middle Manager Edition"
SUB = "Reflect on how you lead change, balance priorities, and enable future readiness."

INTRO = """
In Singapore workplaces, middle managers often sit **at the boundary** — between strategy and execution, stability and change, compliance and innovation.

This reflective quiz helps you notice how you tend to cross boundaries using four mechanisms:

- **Identification (I)** – clarifying purpose, constraints, and direction  
- **Coordination (C)** – building shared routines, plans, and accountability  
- **Reflection (R)** – pausing to understand perspectives and assumptions  
- **Transformation (T)** – trying small experiments to create new practice  

Each scenario is drawn from real Singapore contexts around innovation, service improvement, and transformation.  
Choose what you’d **most likely** do — then see at the end which moves you use most.
"""

FOOTER = "*Inspired by boundary-crossing research (Akkerman & Bakker, 2011).*"
MECH_COLORS = {"I": "#247ba0", "C": "#2aa876", "R": "#f4b400", "T": "#6a4fb3"}

# ============================================================
# 12 SINGAPORE MIDDLE-MANAGER SCENARIOS
# ============================================================
SCENARIOS = [
    {
        "title": "Innovation vs Operations",
        "context": (
            "Your director asks your division to propose an innovative service idea for the next workplan. "
            "Teams are already stretched meeting KPIs, and staff worry innovation will become 'extra work'. "
            "You sense resistance masked as politeness."
        ),
        "why": "Boundary: efficiency vs exploration — delivering today while rethinking tomorrow.",
        "opts": [
            ("Clarify how innovation links to this year’s KPIs — what counts as ‘value add’.", "I"),
            ("Set up a short ideas clinic with small cross-team groups.", "C"),
            ("Ask the team what makes ‘innovation’ feel risky or unrealistic.", "R"),
            ("Pilot one quick idea using existing tools; share results at division meeting.", "T"),
        ],
    },
    {
        "title": "Hierarchy and Voice",
        "context": (
            "In meetings, junior officers rarely challenge senior views. "
            "After a policy rollout, feedback showed ground officers had anticipated the issues but kept silent. "
            "You want more upward feedback without breaking decorum."
        ),
        "why": "Boundary: respect for hierarchy vs psychological safety.",
        "opts": [
            ("Clarify the decision structure — when input is invited vs when direction is fixed.", "I"),
            ("Rotate who presents updates and invite Q&A before management speaks.", "C"),
            ("Ask the team what would make it feel safe to raise tough points early.", "R"),
            ("Create a 'reverse-mentoring' session where juniors critique a process constructively.", "T"),
        ],
    },
    {
        "title": "Digital Transformation Fatigue",
        "context": (
            "Your agency’s new platform promises better citizen experience, but staff see it as another system to learn. "
            "Some quietly revert to old spreadsheets for 'efficiency'."
        ),
        "why": "Boundary: compliance vs ownership — transformation as something done *to* people or *with* them.",
        "opts": [
            ("Restate the ‘why’ — how digital tools connect to mission and workload.", "I"),
            ("Appoint system champions in each team and track adoption pain points.", "C"),
            ("Ask what success would look like for them — not just IT.", "R"),
            ("Co-design one workflow together and measure time saved.", "T"),
        ],
    },
    {
        "title": "Service Excellence vs Staff Well-being",
        "context": (
            "Complaints are rising; leadership pushes for faster responses. "
            "Your team is working late weekly and morale is sliding. "
            "Frontliners feel blamed for systemic issues."
        ),
        "why": "Boundary: service quality vs human sustainability.",
        "opts": [
            ("Clarify service standards and where discretion is allowed.", "I"),
            ("Redesign roster patterns and escalation channels with staff input.", "C"),
            ("Facilitate a discussion: what’s within our control vs structural?", "R"),
            ("Run a one-month pilot to test workload redistribution or automation ideas.", "T"),
        ],
    },
    {
        "title": "Data Sharing Across Divisions",
        "context": (
            "Two departments need to share data for a joint dashboard. "
            "One cites PDPA and prefers email updates; the other needs real-time access for insights."
        ),
        "why": "Boundary: caution vs collaboration.",
        "opts": [
            ("Clarify the data classification and approval lines.", "I"),
            ("Draft a shared SOP and permissions matrix for both divisions.", "C"),
            ("Hold a dialogue on fears about accountability and misuse.", "R"),
            ("Prototype a secure shared folder with restricted fields.", "T"),
        ],
    },
    {
        "title": "Hybrid Work Tensions",
        "context": (
            "Policy mandates three office days. Some staff live far away; others prefer in-person discussions. "
            "You see collaboration dipping but don’t want to micromanage attendance."
        ),
        "why": "Boundary: autonomy vs cohesion.",
        "opts": [
            ("Clarify what activities truly require in-person presence.", "I"),
            ("Create a team charter for hybrid norms everyone signs off.", "C"),
            ("Ask what makes office days valuable or wasteful for each group.", "R"),
            ("Test a rhythm: 2 in-person anchor days tied to core meetings.", "T"),
        ],
    },
    {
        "title": "Performance Conversations",
        "context": (
            "During mid-year reviews, you notice some officers get defensive when feedback touches behaviour. "
            "You want growth, not grievance, but fear hurting relationships."
        ),
        "why": "Boundary: candour vs care.",
        "opts": [
            ("Clarify the difference between developmental and evaluative feedback sessions.", "I"),
            ("Use a structured template focusing on evidence and next steps.", "C"),
            ("Ask them how they prefer to receive feedback and what support helps.", "R"),
            ("Try a ‘feed-forward’ approach — peer-led coaching on one goal for 6 weeks.", "T"),
        ],
    },
    {
        "title": "Procurement and Innovation",
        "context": (
            "A vendor proposes a creative solution but procurement templates can’t capture it easily. "
            "Your colleagues warn: 'Just stick to the usual specs.'"
        ),
        "why": "Boundary: procedural compliance vs creative partnership.",
        "opts": [
            ("Clarify procurement intent — fairness, transparency, value-for-money.", "I"),
            ("Invite Procurement to co-draft an outcome-based requirement with you.", "C"),
            ("Ask why non-standard proposals feel risky; surface assumptions.", "R"),
            ("Pilot a small proof-of-concept under a capped amount.", "T"),
        ],
    },
    {
        "title": "Generational Gap",
        "context": (
            "You lead both long-serving officers and fresh hires. "
            "Meetings split between ‘we tried that before’ and ‘let’s disrupt everything.’"
        ),
        "why": "Boundary: experience vs reinvention.",
        "opts": [
            ("Clarify what must stay (core values) vs what can change.", "I"),
            ("Pair senior and junior staff on one improvement project.", "C"),
            ("Ask each group what they most respect and most misunderstand about the other.", "R"),
            ("Create a 'Then and Now' showcase linking past lessons to current challenges.", "T"),
        ],
    },
    {
        "title": "Citizen Feedback vs Policy Intent",
        "context": (
            "Your team pilots a digital form for faster applications. Citizens find it confusing and complain online. "
            "HQ insists the process is correct; frontline officers face frustration."
        ),
        "why": "Boundary: policy integrity vs citizen experience.",
        "opts": [
            ("Clarify design intent and key constraints with HQ.", "I"),
            ("Set up a feedback loop with daily frontline input to tweak messaging.", "C"),
            ("Ask officers what patterns they observe behind citizen complaints.", "R"),
            ("Prototype a quick explainer guide or video and test with users.", "T"),
        ],
    },
    {
        "title": "Cross-Agency Project",
        "context": (
            "You co-lead a project with another agency. Both agree on purpose but interpret ‘impact’ differently. "
            "Deadlines slip amid polite emails."
        ),
        "why": "Boundary: shared purpose vs divergent measures of success.",
        "opts": [
            ("Clarify the common goal and measurable outcomes in writing.", "I"),
            ("Set up fortnightly syncs to align deliverables and flag tensions early.", "C"),
            ("Ask what success means for each agency and why.", "R"),
            ("Co-design a pilot deliverable to visualise joint success.", "T"),
        ],
    },
    {
        "title": "Future Skills and Reskilling",
        "context": (
            "Your department received funds for skills upgrading, but few officers sign up. "
            "They say they’re too busy or don’t see relevance to their roles."
        ),
        "why": "Boundary: immediate delivery vs long-term growth.",
        "opts": [
            ("Clarify what future skills the organisation truly prioritises.", "I"),
            ("Build a team learning plan linking skills to actual projects.", "C"),
            ("Ask staff what would make learning feel worthwhile or safe to try.", "R"),
            ("Pair skills learning with a real mini-project to apply it immediately.", "T"),
        ],
    },
]

# ============================================================
# MICRO-PRACTICES FOR GROWTH
# ============================================================
MICRO = {
    "I": "Run a **15-min clarity huddle**: purpose, scope, and decision rights before each new project.",
    "C": "Create **one shared process or routine** this month (e.g., tracker, sync, or joint review).",
    "R": "Host a **sense-making pause**: what surprised us, what assumptions changed, what’s next?",
    "T": "Run a **1-week mini-experiment** with your team — test one improvement safely and debrief."
}

# ============================================================
# STATE & SCORING
# ============================================================
def init_state():
    if "order" not in st.session_state:
        st.session_state.order = list(range(len(SCENARIOS)))
        random.shuffle(st.session_state.order)
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {i: None for i in range(len(SCENARIOS))}

def score_mechanisms():
    s = {"I":0,"C":0,"R":0,"T":0}
    for i,a in st.session_state.answers.items():
        if a:
            for (opt,m) in SCENARIOS[i]["opts"]:
                if a == opt:
                    s[m] += 1
    return s

def top_mechs(scores, k=2):
    return [m for m,_ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]]

def low_mechs(scores, k=2):
    return [m for m,_ in sorted(scores.items(), key=lambda x: x[1])[:k]]

# ============================================================
# UI FLOW
# ============================================================
def show_question(i):
    sc = SCENARIOS[i]
    st.markdown(f"### {sc['title']}")
    st.caption(sc["context"])
    with st.expander("Why this is a boundary moment"):
        st.write(sc["why"])
    opts = [o for (o,_) in sc["opts"]]
    prev = st.session_state.answers.get(i)
    idx = opts.index(prev) if prev in opts else 0
    choice = st.radio("Your most likely move:", opts, index=idx, label_visibility="collapsed", key=f"q_{i}")
    c1, c2 = st.columns(2)
    if c1.button("◀ Back", disabled=(st.session_state.page == 0), use_container_width=True):
        st.session_state.page -= 1
        st.rerun()
    if c2.button("Next ▶", use_container_width=True):
        st.session_state.answers[i] = choice
        st.session_state.page += 1
        st.rerun()

def show_results():
    s = score_mechanisms()
    st.success("🎉 You’ve completed your Boundary Compass reflection.")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("I", s["I"]); c2.metric("C", s["C"]); c3.metric("R", s["R"]); c4.metric("T", s["T"])
    fig = go.Figure(go.Bar(x=[s["I"],s["C"],s["R"],s["T"]],
        y=["Identification (I)","Coordination (C)","Reflection (R)","Transformation (T)"],
        orientation="h", marker=dict(color=[MECH_COLORS[k] for k in ["I","C","R","T"]])))
    fig.update_layout(height=360, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)
    names = {"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}
    st.markdown(f"**Where you tend to start:** *{', '.join(names[m] for m in top_mechs(s))}*")
    st.markdown("**Stretch yourself this month:**")
    for m in low_mechs(s):
        st.write(f"- **{names[m]}** — {MICRO[m]}")
    st.divider()
    st.caption(FOOTER)

# ============================================================
# APP ENTRY
# ============================================================
def main():
    apply_css()
    init_state()
    st.title(TITLE)
    st.caption(SUB)
    with st.expander("About this tool", expanded=False):
        st.markdown(INTRO)
    st.progress(st.session_state.page / len(SCENARIOS))
    if st.session_state.page < len(SCENARIOS):
        i = st.session_state.order[st.session_state.page]
        show_question(i)
    else:
        show_results()

if __name__ == "__main__":
    main()