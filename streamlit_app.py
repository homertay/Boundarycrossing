import streamlit as st
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Voyage of Discovery — Ming Leadership", page_icon="🧭", layout="centered")

st.title("🧭 Voyage of Discovery — Ming Leadership Through Boundaries")
st.caption("A 16-scenario, story-driven diagnostic grounded in Akkerman & Bakker’s boundary-crossing mechanisms.")

with st.expander("What this measures (theory → practice)", expanded=False):
    st.markdown("""
**Boundary-Crossing Mechanisms (Akkerman & Bakker, 2011)**  
- **Identification (I)** — seeing differences clearly; naming roles, goals, limits  
- **Coordination (C)** — building bridges: routines, artefacts, agreements  
- **Reflection (R)** — learning via perspective-taking and sense-making  
- **Transformation (T)** — co-creating new practices that integrate worlds  

Leaders develop organisations not by eliminating boundaries, but by **strengthening capacity to work across them**.
""")

# ---------------- Scenarios (16) ----------------
# Each scenario has 4 options, each mapped to I/C/R/T
SCENARIOS = [
    # LENS 1 — Bureaucratic & Hierarchical
    {
        "k": "s1", "icon": "🏯",
        "title": "The Emperor’s Commission (Nanjing, 1405)",
        "blurb": "The Yongle Emperor orders the first great voyage. You must balance ambition and realism in your plan.",
        "opts": [
            ("Present exact logistics and constraints to set expectations.", "I"),
            ("Promise swift success to secure full imperial support.", "C"),
            ("Seek lessons from senior eunuchs who ran prior expeditions.", "R"),
            ("Co-design an adaptive plan with the Ministry of Works.", "T"),
        ],
    },
    {
        "k": "s2", "icon": "📜",
        "title": "The Court’s Doubt (Beijing)",
        "blurb": "Confucian officials criticise the cost of expeditions. Your response will shape political support.",
        "opts": [
            ("Reiterate loyalty to imperial will; obey and proceed.", "I"),
            ("Invite ministers to review shipyards, logs, and stores.", "C"),
            ("Acknowledge their caution; convene a dialogue on risks.", "R"),
            ("Form an advisory council blending naval and scholarly insight.", "T"),
        ],
    },
    {
        "k": "s3", "icon": "🧭",
        "title": "Chain of Command (Yard of Nanjing)",
        "blurb": "Captains below you compete for status and access. Cohesion is fraying.",
        "opts": [
            ("Reassert hierarchy and expected conduct.", "I"),
            ("Clarify reporting lines and cadence of councils.", "C"),
            ("Coach captains privately on shared purpose and roles.", "R"),
            ("Rotate command via a captains’ council to build ownership.", "T"),
        ],
    },
    {
        "k": "s4", "icon": "🌩️",
        "title": "Lessons from Failure (Storm Report)",
        "blurb": "A storm destroys several supply ships. The Emperor awaits your account.",
        "opts": [
            ("Attribute losses to fate and natural hazard.", "I"),
            ("Deliver audit and introduce new safety routines.", "C"),
            ("Hold fleet-wide reflection to surface missed signals.", "R"),
            ("Redesign logistics with shared accountability across teams.", "T"),
        ],
    },

    # LENS 2 — Functional & Technical
    {
        "k": "s5", "icon": "⚓",
        "title": "The Shipwrights’ Dispute (Fujian vs Nanjing)",
        "blurb": "Artisans argue over hull design: proven stability vs speed and cargo efficiency.",
        "opts": [
            ("Choose one proven design for consistency.", "I"),
            ("Standardise blueprints from both schools.", "C"),
            ("Run comparative trials and share results.", "R"),
            ("Commission a hybrid model combining strengths.", "T"),
        ],
    },
    {
        "k": "s6", "icon": "✨",
        "title": "Stars or Compass (Navigation Doctrine)",
        "blurb": "Veterans trust stars; younger crews back the magnetic compass. Doctrine is divided.",
        "opts": [
            ("Keep methods separate; assign by crew preference.", "I"),
            ("Run parallel tests and log performance findings.", "C"),
            ("Facilitate open debate on merits and limits.", "R"),
            ("Integrate both into a new unified navigation doctrine.", "T"),
        ],
    },
    {
        "k": "s7", "icon": "🥖",
        "title": "Supply Shortage in Calicut",
        "blurb": "Merchants hoard grain; engineers warn of rationing. Morale could decay.",
        "opts": [
            ("Impose quota by rank; protect chain of command.", "I"),
            ("Issue daily distribution through officers with records.", "C"),
            ("Hold crew councils to weigh trade-offs and options.", "R"),
            ("Partner with local markets for rapid restock innovation.", "T"),
        ],
    },
    {
        "k": "s8", "icon": "🔔",
        "title": "The Bronze Bell Problem",
        "blurb": "Ritual purity vs practical signaling: bell makers vs sailors.",
        "opts": [
            ("Respect ritual specification as is.", "I"),
            ("Adapt ritual form to naval signaling needs.", "C"),
            ("Dialogue between artisans and sailors on use contexts.", "R"),
            ("Commission a new alloy bell fit for both ceremony and sea.", "T"),
        ],
    },

    # LENS 3 — Cultural & Diplomatic
    {
        "k": "s9", "icon": "🤝",
        "title": "Envoys of Malacca",
        "blurb": "The Sultan requests protection from Siam; the straits are strategic.",
        "opts": [
            ("Issue a decree asserting Ming protection.", "I"),
            ("Formalise protectorate by treaty and escorts.", "C"),
            ("Deepen relationship through cultural exchange first.", "R"),
            ("Train Malaccans to self-defend and co-patrol.", "T"),
        ],
    },
    {
        "k": "s10", "icon": "🦒",
        "title": "The Giraffe from Malindi",
        "blurb": "A giraffe arrives as a wonder-gift from Africa. How do you respond?",
        "opts": [
            ("Parade it as imperial tribute to Heaven’s favour.", "I"),
            ("Catalogue it formally via the Bureau of Rites.", "C"),
            ("Reflect publicly on learning from distant knowledge.", "R"),
            ("Establish envoys for scientific and cultural exchange.", "T"),
        ],
    },
    {
        "k": "s11", "icon": "🏴‍☠️",
        "title": "Pirates or Patriots (Sumatra)",
        "blurb": "Local ‘pirates’ claim to defend native merchants from taxes.",
        "opts": [
            ("Crush rebellion swiftly; reassert order.", "I"),
            ("Offer amnesty if they join Ming patrols.", "C"),
            ("Hear grievances through local councils.", "R"),
            ("Redesign levies with shared governance.", "T"),
        ],
    },
    {
        "k": "s12", "icon": "👑",
        "title": "The King of Ceylon",
        "blurb": "A defiant ruler after an envoy incident; the world watches your next move.",
        "opts": [
            ("Seize the capital to assert order.", "I"),
            ("Negotiate tribute exchange and release.", "C"),
            ("Invite monks to mediate reconciliation.", "R"),
            ("Propose alliance of shared routes and learning.", "T"),
        ],
    },

    # LENS 4 — Ideological & Value
    {
        "k": "s13", "icon": "📚",
        "title": "Confucian vs Maritime Values",
        "blurb": "Scholars warn that overseas trade corrupts virtue; sailors argue prosperity sustains the realm.",
        "opts": [
            ("Uphold restraint; minimise foreign entanglements.", "I"),
            ("Frame trade as benevolence in action (利以義行).", "C"),
            ("Host debates on ethics of maritime expansion.", "R"),
            ("Redefine virtue as outward benevolence (以德服人).", "T"),
        ],
    },
    {
        "k": "s14", "icon": "🧘",
        "title": "Buddhist Monks on Board (Storm)",
        "blurb": "A storm shakes morale; monks chant prayers for safety. Ritual vs routine?",
        "opts": [
            ("Permit prayer but keep ritual minimal.", "I"),
            ("Integrate brief prayer times into ship routine.", "C"),
            ("Reflect on faith’s role in courage with crew.", "R"),
            ("Assign a Harmony Officer for moral well-being.", "T"),
        ],
    },
    {
        "k": "s15", "icon": "🛡️",
        "title": "The Eunuch’s Dilemma",
        "blurb": "Some officers question loyalty to an eunuch commander (you). How do you proceed?",
        "opts": [
            ("Assert imperial mandate directly.", "I"),
            ("Clarify chain of command via imperial edict.", "C"),
            ("Discuss prejudice privately; listen and address concerns.", "R"),
            ("Mentor promising critics into allies.", "T"),
        ],
    },
    {
        "k": "s16", "icon": "🕯️",
        "title": "The Final Voyage (1433)",
        "blurb": "Ageing, you must train successors. What legacy do you leave?",
        "opts": [
            ("Appoint your most loyal subordinate.", "I"),
            ("Build a captains’ council to govern jointly.", "C"),
            ("Lead a fleet-wide reflection on lessons and ethos.", "R"),
            ("Empower next generation to define a new mission.", "T"),
        ],
    },
]

# ------------ State -------------
if "order" not in st.session_state:
    st.session_state.order = list(range(len(SCENARIOS)))
    random.shuffle(st.session_state.order)
    st.session_state.page = 0
    # Pre-fill answers dict with None so Back/Next stays stable
    st.session_state.answers = {idx: None for idx in range(len(SCENARIOS))}

TOTAL = len(SCENARIOS)

# ------------ Helpers ----------
def show_scenario(idx: int):
    sc = SCENARIOS[idx]
    st.markdown(f"### {sc['icon']} {sc['title']}")
    st.write(sc["blurb"])

    # Restore previous choice if exists
    prev = st.session_state.answers.get(idx, None)
    options = [o for (o, m) in sc["opts"]]
    default_index = options.index(prev) if prev in options else None

    choice = st.radio(
        "Your decision:",
        options,
        index=default_index,
        label_visibility="collapsed",
        key=f"radio_{idx}"
    )

    col1, col2 = st.columns(2)
    with col1:
        disabled_back = st.session_state.page <= 0
        if st.button("◀ Back", disabled=disabled_back, use_container_width=True):
            st.session_state.page -= 1
            st.experimental_rerun()
    with col2:
        if st.button("Next ▶", use_container_width=True):
            if choice is None:
                st.warning("Please choose an option to continue.")
            else:
                st.session_state.answers[idx] = choice
                st.session_state.page += 1
                st.experimental_rerun()

def compute_scores():
    scores = {"I": 0, "C": 0, "R": 0, "T": 0}
    for i, ans in st.session_state.answers.items():
        if ans is None:
            continue
        for (o, m) in SCENARIOS[i]["opts"]:
            if o == ans:
                scores[m] += 1
                break
    return scores

def archetype_from(scores):
    items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary, second = items[0][0], items[1][0]
    spread = items[0][1] - items[-1][1]
    if spread <= 1:
        # balanced → coalition leadership vibe
        return "DN"

    # 8 archetypes: 4 pure + 4 hybrids (IC, IR, CR, CT) + balanced mapped to DN
    pair = primary + second
    mapping = {
        "IC": "SN", "IR": "ICa", "CR": "DN", "CT": "BI",
        "I": "BM", "C": "BAc", "R": "RH", "T": "EC"
    }
    return mapping.get(pair, mapping[primary])

ARCH = {
    "BM": ("🗺 Boundary Mapper", "You clarify identity, language, and expectations; others rely on your steadiness."),
    "BAc": ("🔗 Bridge Architect", "You connect people and systems through routines and shared tools."),
    "RH": ("🪞 Reflective Helmsman", "You lead through empathy and sense-making; you turn tension into insight."),
    "EC": ("🌾 Ecosystem Catalyst", "You integrate worlds and prototype new practices that stick."),
    "SN": ("🧭 System Navigator", "You align strategy, people, and process; you bring order from complexity."),
    "ICa": ("🧩 Insight Cartographer", "You map human and cultural nuances into shared understanding."),
    "DN": ("🪞➡️🔗 Diplomatic Navigator", "You balance empathy with structure; trusted in cross-team coalitions."),
    "BI": ("🛠 Bridge Innovator", "You turn promising ideas into systems that scale without chaos."),
}

def bar_chart(scores):
    # Simple, clear horizontal bar chart of the four markers
    cats = ["Identification (I)", "Coordination (C)", "Reflection (R)", "Transformation (T)"]
    vals = [scores["I"], scores["C"], scores["R"], scores["T"]]
    fig = go.Figure(go.Bar(
        x=vals, y=cats, orientation="h",
        marker=dict(line=dict(width=0.5, color="#333"))
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Selections", yaxis_title="Mechanisms",
        height=320
    )
    return fig

def show_results():
    st.success("🌊 Voyage complete!")
    scores = compute_scores()

    # Four big markers first
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("I", scores["I"])
    c2.metric("C", scores["C"])
    c3.metric("R", scores["R"])
    c4.metric("T", scores["T"])

    # Clear horizontal bar chart (no compass/radar)
    st.plotly_chart(bar_chart(scores), use_container_width=True)

    code = archetype_from(scores)
    name, desc = ARCH[code]
    st.header(name)
    st.write(desc)
    st.markdown("> **Reflection prompt:** Which boundary could become a site of learning in your current context — and what will you do next?")

# ------------ Flow -------------
if "page" not in st.session_state:
    st.session_state.page = 0

st.progress(st.session_state.page / TOTAL)

if st.session_state.page < TOTAL:
    idx = st.session_state.order[st.session_state.page]
    show_scenario(idx)
else:
    show_results()