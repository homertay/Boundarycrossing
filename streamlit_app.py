import streamlit as st
import plotly.graph_objects as go
from dataclasses import dataclass

# ------------------------------------------------------------
# Theoretical frame (Akkerman & Bakker, 2011):
#   Identification · Coordination · Reflection · Transformation
# Each scenario option maps to one mechanism.
# ------------------------------------------------------------

st.set_page_config(page_title="Voyage of Discovery: Boundary-Crossing Diagnostic",
                   page_icon="🧭", layout="centered")

st.title("🧭 Voyage of Discovery: Boundary-Crossing Diagnostic")
st.caption("A short, scenario-based assessment grounded in boundary-crossing theory (Akkerman & Bakker, 2011).")

with st.expander("What this measures (theory → practice)", expanded=False):
    st.markdown("""
- **Identification** — seeing differences clearly; naming roles, goals, and limits.  
- **Coordination** — building bridges (shared routines, artefacts, and agreements).  
- **Reflection** — learning via perspective-taking; double-loop learning.  
- **Transformation** — co-creating new practices that integrate worlds.  
Each scenario presents four legitimate leadership moves, *one per mechanism*.
""")

# -------------------- Scenario model --------------------
@dataclass
class Scenario:
    key: str
    title: str
    blurb: str
    options: list  # list of (label, mechanism)

SCENARIOS = [
    Scenario(
        key="s1",
        title="1) The Crew Before Departure (Nanjing, 1410)",
        blurb=("Time is short before sailing. Your crew are loyal but many are strangers to each other. "
               "You can only choose one approach before leaving port."),
        options=[
            ("Personally meet small groups to learn their stories and expectations.", "Identification"),
            ("Host a grand banquet so everyone bonds through celebration.", "Coordination"),
            ("Ask lieutenants to observe morale while you focus on logistics.", "Reflection"),
            ("Launch a co-authored 'Fleet Code' that defines shared purpose.", "Transformation"),
        ],
    ),
    Scenario(
        key="s2",
        title="2) The Dragon Captains Arrive",
        blurb=("Reinforcements trained in the Dragon style join your Phoenix-style fleet. Cohesion hangs in the balance."),
        options=[
            ("Let Dragon captains keep their style as long as orders are obeyed.", "Identification"),
            ("Standardise immediately: all ships adopt Phoenix methods.", "Coordination"),
            ("Create a mixed council to design hybrid manoeuvres together.", "Transformation"),
            ("Observe both styles in action before deciding.", "Reflection"),
        ],
    ),
    Scenario(
        key="s3",
        title="3) Ping and Wong’s Dispute",
        blurb=("Two senior officers clash: Wong urges caution; Ping pushes innovation. Their tension spreads and both seek your ruling."),
        options=[
            ("Side with Wong: safety first; discipline keeps fleets alive.", "Identification"),
            ("Support Ping’s experiment: progress needs boldness.", "Transformation"),
            ("Convene both to co-design a blended solution they present jointly.", "Coordination"),
            ("Coach each privately to see the other’s perspective.", "Reflection"),
        ],
    ),
    Scenario(
        key="s4",
        title="4) Fei, the Quiet Innovator",
        blurb=("A junior cartographer (Fei) secretly improves outdated maps but fears public attention. How do you handle his contribution?"),
        options=[
            ("Announce the improvement yourself, crediting Fei publicly.", "Coordination"),
            ("Co-present with Fei at the next briefing; support his stretch.", "Reflection"),
            ("Ask Fei to lead the presentation; empower him into visibility.", "Transformation"),
            ("Praise Fei privately; honour his comfort and boundaries.", "Identification"),
        ],
    ),
    Scenario(
        key="s5",
        title="5) Pirates in the Straits of Malacca",
        blurb=("Pirates terrorise trade near Malacca. The Sultan begs for help. Your response will shape Ming’s legacy."),
        options=[
            ("Launch the full fleet to crush the pirate strongholds decisively.", "Coordination"),
            ("Deploy a Ming squadron to train Malacca’s sailors to defend themselves.", "Transformation"),
            ("Lead joint patrols, alternating command and sharing tactics.", "Reflection"),
            ("Send arms and supplies; let Malacca manage its own defence.", "Identification"),
        ],
    ),
]

# -------------------- State --------------------
if "answers" not in st.session_state:
    st.session_state.answers = {}

st.markdown("### Make your choices")
st.write("Each scenario offers four **legitimate** leadership moves. Choose what you would most likely do.")

# Render scenarios
for sc in SCENARIOS:
    st.markdown(f"#### {sc.title}")
    st.write(sc.blurb)
    choice = st.radio("Your decision:", [opt for opt, mech in sc.options],
                      key=f"radio_{sc.key}", index=None, label_visibility="collapsed")
    st.session_state.answers[sc.key] = choice
    st.divider()

# -------------------- Submit --------------------
if st.button("See my leadership profile"):
    # Check all answered
    unanswered = [s.title for s in SCENARIOS if not st.session_state.answers.get(s.key)]
    if unanswered:
        st.error("Please answer all scenarios to continue.")
        st.stop()

    # Score mechanisms
    scores = {"Identification":0, "Coordination":0, "Reflection":0, "Transformation":0}
    for sc in SCENARIOS:
        choice = st.session_state.answers[sc.key]
        mech = next(m for (opt,m) in sc.options if opt == choice)
        scores[mech] += 1

    # Radar chart
    st.subheader("Your boundary-crossing mechanism profile")
    cats = list(scores.keys())
    vals = [scores[c] for c in cats]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals+[vals[0]], theta=cats+[cats[0]], fill='toself', name='Profile'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,5])), showlegend=False,
                      margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- Archetype mapping ----------------
    archetypes = {
        "Boundary Mapper": {
            "sig": ("Identification",),
            "emoji": "🗺",
            "desc": "You define edges clearly and give language to differences. People rely on you to bring order when things blur.",
            "stretch": "Move from describing boundaries to designing one concrete crossing (ritual, artefact, or shared metric)."
        },
        "Bridge Architect": {
            "sig": ("Coordination",),
            "emoji": "🔗",
            "desc": "You connect people and systems through routines, agreements, and shared tools. You turn conflict into workflow.",
            "stretch": "Balance process with purpose—open with a shared ‘why’, not only the ‘how’."
        },
        "Reflective Helmsman": {
            "sig": ("Reflection",),
            "emoji": "🪞",
            "desc": "You learn by listening and reframing. Your calm, perspective-taking presence creates psychological safety under pressure.",
            "stretch": "Translate reflection into one visible shift in behaviour, metric, or decision."
        },
        "Ecosystem Catalyst": {
            "sig": ("Transformation",),
            "emoji": "🌾",
            "desc": "You integrate worlds and prototype new practices. People move with you because change feels purposeful, not chaotic.",
            "stretch": "Codify what works so others can adopt it—a one-page pattern or checklist."
        },
        "Diplomatic Navigator": {
            "sig": ("Coordination","Reflection"),
            "emoji": "🧭",
            "desc": "You balance empathy with structure. You orchestrate alliances and keep diverse groups moving without losing trust.",
            "stretch": "Experiment sooner with small pilots—let action inform consensus."
        },
        "Integrative Weaver": {
            "sig": ("Identification","Coordination","Reflection","Transformation"),
            "emoji": "🕸",
            "desc": "You move fluidly across mapping, bridging, reflecting, and transforming. You mentor others to cross boundaries with you.",
            "stretch": "Protect your energy—build pathways so weaving continues beyond you."
        }
    }

    # Decide archetype
    # If scores are all within 1 point → Weaver
    if max(scores.values()) - min(scores.values()) <= 1:
        archetype = "Integrative Weaver"
    else:
        # Diplomatic Navigator if C and R tie for top (or near-top) and exceed others
        if abs(scores["Coordination"] - scores["Reflection"]) == 0 and \
           scores["Coordination"] >= max(scores["Identification"], scores["Transformation"]):
            archetype = "Diplomatic Navigator"
        else:
            top_mech = max(scores, key=scores.get)
            mapping = {
                "Identification":"Boundary Mapper",
                "Coordination":"Bridge Architect",
                "Reflection":"Reflective Helmsman",
                "Transformation":"Ecosystem Catalyst"
            }
            archetype = mapping[top_mech]

    info = archetypes[archetype]
    st.markdown(f"## Your leadership archetype: {info['emoji']} **{archetype}**")
    st.write(info["desc"])
    st.markdown(f"**Stretch practice:** {info['stretch']}")

    st.markdown("> **Reflection prompt:** Where in your current voyage (team, project, classroom) could you cross one boundary this month?")

    st.markdown("---")
    with st.expander("Theory sources", expanded=False):
        st.markdown("""
- Akkerman, S. & Bakker, A. (2011). Boundary crossing & boundary objects.  
- Star, S. L. & Griesemer, J. (1989). Boundary objects.  
- Carlile, P. (2004). Knowledge boundaries.  
- Wenger, E. (1998). Communities of Practice (brokering).
""")