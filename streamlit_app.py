import streamlit as st
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Voyage of Discovery — Ming Leadership", page_icon="🧭", layout="centered")

st.title("🧭 Voyage of Discovery — Ming Leadership Through Boundaries")
st.caption("A 16-scenario, story-driven diagnostic grounded in Akkerman & Bakker’s boundary-crossing mechanisms.")

with st.expander("What this measures (theory → practice)", expanded=False):
    st.markdown("""
**Boundary-Crossing Mechanisms (Akkerman & Bakker, 2011)**  
- **Identification (I)** — seeing differences clearly; naming roles, goals, limits.  
- **Coordination (C)** — building bridges via shared routines, artefacts, agreements.  
- **Reflection (R)** — learning through perspective-taking and sense-making.  
- **Transformation (T)** — co-creating new practices that integrate worlds.  

Leaders develop organisations not by eliminating boundaries, but by **strengthening capacity to work across them**.
""")

# ---------------- Scenarios (16) ----------------
SCENARIOS = [
    # LENS 1 — Bureaucratic & Hierarchical
    {
        "k": "s1",
        "title": "The Emperor’s Commission (Nanjing, 1405)",
        "img": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=1600&q=80&auto=format&fit=crop",
        "blurb": "The Yongle Emperor orders the first great voyage. You must balance ambition and realism in your plan.",
        "opts": [
            ("Present exact logistics and constraints to set expectations.", "I"),
            ("Promise swift success to secure full imperial support.", "C"),
            ("Seek lessons from senior eunuchs who ran prior expeditions.", "R"),
            ("Co-design an adaptive plan with the Ministry of Works.", "T"),
        ],
    },
    {
        "k": "s2",
        "title": "The Court’s Doubt (Beijing)",
        "img": "https://images.unsplash.com/photo-1520975916090-3105956dac38?w=1600&q=80&auto=format&fit=crop",
        "blurb": "Confucian officials criticise the cost of expeditions. Your response will shape political support.",
        "opts": [
            ("Reiterate loyalty to imperial will; obey and proceed.", "I"),
            ("Invite ministers to review shipyards, logs, and stores.", "C"),
            ("Acknowledge their caution; convene a dialogue on risks.", "R"),
            ("Form an advisory council blending naval and scholarly insight.", "T"),
        ],
    },
    {
        "k": "s3",
        "title": "Chain of Command (Yard of Nanjing)",
        "img": "https://images.unsplash.com/photo-1495197359483-d092478c170a?w=1600&q=80&auto=format&fit=crop",
        "blurb": "Captains below you compete for status and access. Cohesion is fraying.",
        "opts": [
            ("Reassert hierarchy and expected conduct.", "I"),
            ("Clarify reporting lines and cadence of councils.", "C"),
            ("Coach captains privately on shared purpose and roles.", "R"),
            ("Rotate command via a captains’ council to build ownership.", "T"),
        ],
    },
    {
        "k": "s4",
        "title": "Lessons from Failure (Storm Report)",
        "img": "https://images.unsplash.com/photo-1505839673365-e3971f8d9184?w=1600&q=80&auto=format&fit=crop",
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
        "k": "s5",
        "title": "The Shipwrights’ Dispute (Fujian vs Nanjing)",
        "img": "https://images.unsplash.com/photo-1482192596544-9eb780fc7f66?w=1600&q=80&auto=format&fit=crop",
        "blurb": "Artisans argue over hull design: proven stability vs speed and cargo efficiency.",
        "opts": [
            ("Choose one proven design for consistency.", "I"),
            ("Standardise blueprints from both schools.", "C"),
            ("Run comparative trials and share results.", "R"),
            ("Commission a hybrid model combining strengths.", "T"),
        ],
    },
    {
        "k": "s6",
        "title": "Stars or Compass (Navigation Doctrine)",
        "img": "https://images.unsplash.com/photo-1482192505345-5655af888cc4?w=1600&q=80&auto=format&fit=crop",
        "blurb": "Veterans trust stars; younger crews back the magnetic compass. Doctrine is divided.",
        "opts": [
            ("Keep methods separate; assign by crew preference.", "I"),
            ("Run parallel tests and log performance findings.", "C"),
            ("Facilitate open debate on merits and limits.", "R"),
            ("Integrate both into a new unified navigation doctrine.", "T"),
        ],
    },
    {
        "k": "s7",
        "title": "Supply Shortage in Calicut",
        "img": "https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=1600&q=80&auto=format&fit=crop",
        "blurb": "Merchants hoard grain; engineers warn of rationing. Morale could decay.",
        "opts": [
            ("Impose quota by rank; protect chain of command.", "I"),
            ("Issue daily distribution through officers with records.", "C"),
            ("Hold crew councils to weigh trade-offs and options.", "R"),
            ("Partner with local markets for rapid restock innovation.", "T"),
        ],
    },
    {
        "k": "s8",
        "title": "The Bronze Bell Problem",
        "img": "https://images.unsplash.com/photo-1500534623283-312aade485b7?w=1600&q=80&auto=format&fit=crop",
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
        "k": "s9",
        "title": "Envoys of Malacca",
        "img": "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1600&q=80&auto=format&fit=crop",
        "blurb": "The Sultan requests protection from Siam; the straits are strategic.",
        "opts": [
            ("Issue a decree asserting Ming protection.", "I"),
            ("Formalise protectorate by treaty and escorts.", "C"),
            ("Deepen relationship through cultural exchange first.", "R"),
            ("Train Malaccans to self-defend and co-patrol.", "T"),
        ],
    },
    {
        "k": "s10",
        "title": "The Giraffe from Malindi",
        "img": "https://images.unsplash.com/photo-1533113354690-2099c8242f24?w=1600&q=80&auto=format&fit=crop",
        "blurb": "A giraffe arrives as a wonder-gift from Africa. How do you respond?",
        "opts": [
            ("Parade it as imperial tribute to Heaven’s favour.", "I"),
            ("Catalogue it formally via the Bureau of Rites.", "C"),
            ("Reflect publicly on learning from distant knowledge.", "R"),
            ("Establish envoys for scientific and cultural exchange.", "T"),
        ],
    },
    {
        "k": "s11",
        "title": "Pirates or Patriots (Sumatra)",
        "img": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1600&q=80&auto=format&fit=crop",
        "blurb": "Local ‘pirates’ claim to defend native merchants from taxes.",
        "opts": [
            ("Crush rebellion swiftly; reassert order.", "I"),
            ("Offer amnesty if they join Ming patrols.", "C"),
            ("Hear grievances through local councils.", "R"),
            ("Redesign levies with shared governance.", "T"),
        ],
    },
    {
        "k": "s12",
        "title": "The King of Ceylon",
        "img": "https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=1600&q=80&auto=format&fit=crop",
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
        "k": "s13",
        "title": "Confucian vs Maritime Values",
        "img": "https://images.unsplash.com/photo-1500534668822-8b9510587c7b?w=1600&q=80&auto=format&fit=crop",
        "blurb": "Scholars warn that overseas trade corrupts virtue; sailors argue prosperity sustains the realm.",
        "opts": [
            ("Uphold restraint; minimise foreign entanglements.", "I"),
            ("Frame trade as benevolence in action (利以義行).", "C"),
            ("Host debates on ethics of maritime expansion.", "R"),
            ("Redefine virtue as outward benevolence (以德服人).", "T"),
        ],
    },
    {
        "k": "s14",
        "title": "Buddhist Monks on Board (Storm)",
        "img": "https://images.unsplash.com/photo-1481349518771-20055b2a7b24?w=1600&q=80&auto=format&fit=crop",
        "blurb": "A storm shakes morale; monks chant prayers for safety. Ritual vs routine?",
        "opts": [
            ("Permit prayer but keep ritual minimal.", "I"),
            ("Integrate brief prayer times into ship routine.", "C"),
            ("Reflect on faith’s role in courage with crew.", "R"),
            ("Assign a Harmony Officer for moral well-being.", "T"),
        ],
    },
    {
        "k": "s15",
        "title": "The Eunuch’s Dilemma",
        "img": "https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?w=1600&q=80&auto=format&fit=crop",
        "blurb": "Some officers question loyalty to an eunuch commander (you). How do you proceed?",
        "opts": [
            ("Assert imperial mandate directly.", "I"),
            ("Clarify chain of command via imperial edict.", "C"),
            ("Discuss prejudice privately; listen and address concerns.", "R"),
            ("Mentor promising critics into allies.", "T"),
        ],
    },
    {
        "k": "s16",
        "title": "The Final Voyage (1433)",
        "img": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1600&q=80&auto=format&fit=crop",
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
    st.session_state.answers = {}

TOTAL = len(SCENARIOS)

# ------------ Functions ----------
def show_scenario(idx):
    sc = SCENARIOS[idx]
    st.image(sc["img"], use_column_width=True, caption=sc["title"])
    st.markdown(f"### {sc['title']}")
    st.write(sc["blurb"])
    choice = st.radio("Your decision:", [o for (o, m) in sc["opts"]], index=None, label_visibility="collapsed", key=f"r_{idx}")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.page > 0 and st.button("◀ Back"):
            st.session_state.page -= 1
            st.experimental_rerun()
    with col2:
        if st.button("Next ▶"):
            if choice is None:
                st.warning("Please choose an option to continue.")
            else:
                st.session_state.answers[idx] = choice
                st.session_state.page += 1
                st.experimental_rerun()

def compute_scores():
    scores = {"I":0,"C":0,"R":0,"T":0}
    for i, ans in st.session_state.answers.items():
        for (o,m) in SCENARIOS[i]["opts"]:
            if o == ans:
                scores[m] += 1
    return scores

def boundary_compass(scores):
    x = scores["T"] - scores["C"]
    y = scores["R"] - scores["I"]
    fig = go.Figure()
    fig.add_shape(type="line", x0=-8, x1=8, y0=0, y1=0, line=dict(color="#999"))
    fig.add_shape(type="line", x0=0, x1=0, y0=-8, y1=8, line=dict(color="#999"))
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=14), name="You"))
    fig.update_layout(
        xaxis=dict(title="Structure ←  C   |   T  → Emergence", range=[-8,8]),
        yaxis=dict(title="Self/Role ←  I   |   R  → Other/System", range=[-8,8]),
        showlegend=False, height=420)
    return fig

ARCH = {
    "BM": ("🗺 Boundary Mapper","You clarify identity, language, and expectations; others rely on your steadiness."),
    "BAc": ("🔗 Bridge Architect","You connect people and systems through routines and shared tools."),
    "RH": ("🪞 Reflective Helmsman","You lead through empathy and sense-making; you turn tension into insight."),
    "EC": ("🌾 Ecosystem Catalyst","You integrate worlds and prototype new practices that stick."),
    "SN": ("🧭 System Navigator","You align strategy, people, and process; you bring order from complexity."),
    "ICa": ("🧩 Insight Cartographer","You map human and cultural nuances into shared understanding."),
    "DN": ("🪞➡️🔗 Diplomatic Navigator","You balance empathy with structure; trusted in cross-team coalitions."),
    "BI": ("🛠 Bridge Innovator","You turn promising ideas into systems that scale without chaos."),
}

def archetype_from(scores):
    items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary, secondary = items[0][0], items[1][0]
    spread = items[0][1]-items[-1][1]
    if spread <= 1:
        return "DN"
    pair = primary+secondary
    mapping = {"IC":"SN","IR":"ICa","CR":"DN","CT":"BI","RT":"EC","IT":"SN"}
    return mapping.get(pair, {"I":"BM","C":"BAc","R":"RH","T":"EC"}[primary])

def show_results():
    st.success("🌊 Voyage complete!")
    scores = compute_scores()
    st.write("#### Your boundary crossings summary")
    st.plotly_chart(boundary_compass(scores), use_container_width=True)
    code = archetype_from(scores)
    name, desc = ARCH[code]
    st.header(name)
    st.write(desc)
    st.markdown("> **Reflection prompt:** Which boundaries in your own work today could become sites of learning and innovation?")

# ------------ Flow -------------
st.progress(st.session_state.page / TOTAL)
if st.session_state.page < TOTAL:
    idx = st.session_state.order[st.session_state.page]
    show_scenario(idx)
else:
    show_results()