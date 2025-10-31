import streamlit as st
import plotly.graph_objects as go
import random, json
from datetime import datetime

# ------------------------------------------------------------
# App configuration
# ------------------------------------------------------------
st.set_page_config(page_title="The Boundary Compass", page_icon="🧭", layout="centered")

TITLE = "🧭 The Boundary Compass — Learning at the Edge"
SUB = "Explore your boundary-crossing style across sticky, real-world dilemmas."

# ------------------------------------------------------------
# Utility text
# ------------------------------------------------------------
INTRO = """
**Why this game?**

In complex work, many problems live at **boundaries** — between roles, functions, values, or systems.
Research shows that learning at these edges tends to happen through four mechanisms:

- **Identification (I)** — seeing and naming differences & boundaries clearly  
- **Coordination (C)** — building shared routines, tools, and agreements  
- **Reflection (R)** — making sense across perspectives through dialogue  
- **Transformation (T)** — prototyping hybrid practices and embedding change  

Choose what you would **most likely** do in each scenario. At the end, you’ll see your
**Boundary Compass** profile, a **leadership archetype**, and stretch prompts to grow.
"""

FOOTER = """
*Boundary Compass mechanisms based on educational research on boundary crossing and boundary objects
(Akkerman & Bakker, 2011).*  
"""

# ------------------------------------------------------------
# Scenario bank — 12 Singapore/ASEAN-sensitive "sticky/wicked" dilemmas
# Each scenario: title, context (short), why_tricky, options[(label, mechanism)]
# ------------------------------------------------------------
SCENARIOS = [
    {
        "key": "s1",
        "title": "AI & Ethics — Mis-send Incident",
        "context": "A GenAI assistant improves speed, but one draft email with customer data was auto-sent to the wrong party.",
        "why": "Speed, ethics, and trust collide; compliance wants a pause, business wants a fast fix.",
        "opts": [
            ("Pause AI usage temporarily and restate the governance boundary.", "I"),
            ("Introduce a human review step and a data-steward role before sends.", "C"),
            ("Facilitate a learning debrief on trust, oversight and accountability.", "R"),
            ("Redesign the workflow: ethical guardrails + literacy training + pipeline checks.", "T"),
        ],
    },
    {
        "key": "s2",
        "title": "Psychological Safety — Broken Promise",
        "context": "A staff member shared candidly in a 'speak-up' session; later it appeared in her performance review.",
        "why": "The formal system undermined the informal one; trust suffered.",
        "opts": [
            ("Clarify the rule: feedback spaces are confidential and non-evaluative.", "I"),
            ("Co-create and publish a 'safe dialogue' code co-owned by HR and managers.", "C"),
            ("Hold a reflective conversation about fear and safety in this context.", "R"),
            ("Design a new feedback process: anonymised channels + peer-led debriefs.", "T"),
        ],
    },
    {
        "key": "s3",
        "title": "Burnout vs Performance — Hero Culture",
        "context": "One team hits targets by routinely working nights/weekends; leaders praise 'commitment'. Others push back.",
        "why": "Productivity signals clash with sustainability and wellbeing.",
        "opts": [
            ("Reaffirm that wellbeing is non-negotiable; define red lines.", "I"),
            ("Track workload/rest in a transparent dashboard (not just output).", "C"),
            ("Invite stories: what do we believe about sacrifice and success?", "R"),
            ("Pilot 'deep-work weeks' that reward efficiency over hours, then codify.", "T"),
        ],
    },
    {
        "key": "s4",
        "title": "Diversity Fatigue — Purple Parade",
        "context": "Annual inclusion activities aligned with The Purple Parade see low engagement; some call it 'symbolic'.",
        "why": "Good intent, weak resonance; inclusion risks performativity.",
        "opts": [
            ("Re-articulate the purpose: accessibility, belonging, and impact (not optics).", "I"),
            ("Form a cross-functional inclusion team to co-design meaningful actions.", "C"),
            ("Use story circles: hear lived experiences and barriers staff face.", "R"),
            ("Shift from 'event day' to year-round practices (accessibility reviews, hiring).", "T"),
        ],
    },
    {
        "key": "s5",
        "title": "Regulation vs Innovation — MAS Uncertainty",
        "context": "A fintech idea uses digital IDs; Compliance blocks it, citing unclear MAS guidance; CEO asks 'find a way'.",
        "why": "Legal-risk vs innovation ambition; ambiguity is real.",
        "opts": [
            ("Define non-negotiables clearly: what rules forbid vs what’s unclear.", "I"),
            ("Stand up a 'sandbox' charter with checkpoints and shared criteria.", "C"),
            ("Host a dialogue on risk appetite across teams; surface assumptions.", "R"),
            ("Prototype a low-risk variant within guidelines to test assumptions.", "T"),
        ],
    },
    {
        "key": "s6",
        "title": "Regional Inequity — Bonus Benchmarks",
        "context": "HQ sets bonuses pegged to global markets; ASEAN branches feel unseen.",
        "why": "Justice, power, and belonging across regions.",
        "opts": [
            ("Name the inequity and define fairness across contexts explicitly.", "I"),
            ("Create a transparent weighting matrix for different economies.", "C"),
            ("Run reflection circles on value and recognition regionally.", "R"),
            ("Co-create a differentiated rewards framework with HQ & local leaders.", "T"),
        ],
    },
    {
        "key": "s7",
        "title": "Toxic Talent — High Performance, Low Respect",
        "context": "A star leader drives revenue but mistreats people; complaints are mounting.",
        "why": "Loyalty and fear vs culture and values; moral injury risk.",
        "opts": [
            ("Clarify zero-tolerance values and what 'performance' includes.", "I"),
            ("Establish a fair escalation/remediation protocol with Ethics & Legal.", "C"),
            ("Facilitate a reflective session on courage, fear, and complicity.", "R"),
            ("Shift metrics from solitary heroism to team-based performance.", "T"),
        ],
    },
    {
        "key": "s8",
        "title": "Digital Divide — Intergenerational Tension",
        "context": "New systems roll out fast; senior colleagues feel left behind; jokes about 'boomer pace'.",
        "why": "Capability gap + stereotypes; retention risk of experience.",
        "opts": [
            ("Set the inclusion boundary: no ageism; learning is for all.", "I"),
            ("Pair younger 'digital coaches' with senior staff; schedule learning blocks.", "C"),
            ("Hold a perspective-taking dialogue on biases and strengths.", "R"),
            ("Launch an intergenerational innovation project and embed the model.", "T"),
        ],
    },
    {
        "key": "s9",
        "title": "Environmental Accountability — Green Claims",
        "context": "Marketing touts 'green finance' but portfolio still includes heavy emitters.",
        "why": "Reputation vs reality; integrity risk.",
        "opts": [
            ("Restate what counts as 'green' under the taxonomy; draw the line.", "I"),
            ("Create an ESG validation checklist linking Sustainability/Risk/Marketing.", "C"),
            ("Reflect: where is aspiration vs deception? Capture learning.", "R"),
            ("Redesign products with measurable ESG criteria and reporting.", "T"),
        ],
    },
    {
        "key": "s10",
        "title": "Leadership Succession — Legacy vs Governance",
        "context": "CEO wants protégé as successor; board favours external candidate.",
        "why": "Power, loyalty, trust in process.",
        "opts": [
            ("Clarify decision rights (board vs CEO inputs); publish the process.", "I"),
            ("Set transparent criteria and a structured assessment flow.", "C"),
            ("Host a facilitated reflection on legacy, identity, and the future state.", "R"),
            ("Design a co-transition: mentoring plan + integration roadmap.", "T"),
        ],
    },
    {
        "key": "s11",
        "title": "Sustainability Trade-off — Green Goals vs Growth",
        "context": "Net-zero pledge meets a profitable project (data-centre expansion) that raises near-term emissions.",
        "why": "Purpose, profit, and credibility collide.",
        "opts": [
            ("Re-articulate the sustainability boundary: taxonomy, thresholds, red lines.", "I"),
            ("Co-create a decision playbook with Finance/Risk/Sustainability.", "C"),
            ("Host a conscience dialogue: 'What message do we send?'", "R"),
            ("Propose profit × carbon-intensity metrics; pilot sustainability-linked financing.", "T"),
        ],
    },
    {
        "key": "s12",
        "title": "Public Failure — Viral Outage",
        "context": "A payroll glitch delays salaries; social media erupts; PR wants silence; customers want honesty.",
        "why": "Legal caution vs moral accountability; speed vs accuracy.",
        "opts": [
            ("Define truth boundaries: what can be shared when.", "I"),
            ("Form a Legal-PR-Ops war-room with joint response SOP.", "C"),
            ("Reflect internally on fear, blame, and public trust.", "R"),
            ("Publish a transparent disclosure template and follow through.", "T"),
        ],
    },
]

# ------------------------------------------------------------
# Archetypes (SG-flavoured) and stretch guidance
# ------------------------------------------------------------
ARCHETYPES = {
    "IT": ("🧩 Lego Synthesiser", "You integrate old and new wisely, re-assembling pieces into better forms."),
    "IC": ("🎫 EZ-Link Navigator", "You read systems quickly and help people move through rules and structures."),
    "CR": ("🧂 Condiment Connector", "You blend people and process; things go smoother when you’re around."),
    "RT": ("🥫 Milo Tin Transformer", "You learn fast and repurpose experience into creative new practice."),
    "IR": ("🪞 Kopitiam Mirror", "You surface assumptions and help others see clearly — with care and humour."),
    "CT": ("🧰 Swiss Knife Collaborator", "You make innovation operational — bridging ideas into routines."),
    "ALL": ("🌀 Boundary Alchemist", "You flex across all four mechanisms and catalyse learning in others."),
    "LOW": ("🪑 The Settler", "You stabilise the space; with gentle stretch you’ll expand your range."),
}

MICRO_PRACTICES = {
    "I": "Before the next project, write a one-page 'boundary brief': purpose, roles, red lines, and decision rights.",
    "C": "Create one simple boundary object this month (shared checklist, glossary, or ritual) that others can re-use.",
    "R": "Run a 20-min 'sense-making huddle' after a meeting: What surprised us? What assumptions were exposed?",
    "T": "Prototype a small hybrid change; embed it as a repeatable routine if it works.",
}

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------
def init_state():
    if "order" not in st.session_state:
        st.session_state.order = list(range(len(SCENARIOS)))
        random.shuffle(st.session_state.order)
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {i: None for i in range(len(SCENARIOS))}

def score_mechanisms():
    scores = {"I": 0, "C": 0, "R": 0, "T": 0}
    for i, ans in st.session_state.answers.items():
        if ans is None:
            continue
        for (label, mech) in SCENARIOS[i]["opts"]:
            if ans == label:
                scores[mech] += 1
                break
    return scores

def pick_archetype(scores):
    vals = list(scores.values())
    spread = max(vals) - min(vals)
    if spread <= 1:
        return "ALL"  # Boundary Alchemist — balanced profile
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary, secondary = ordered[0][0], ordered[1][0]
    pair = primary + secondary
    # Map to SG-flavoured duo types
    mapping = {
        "IT": "IT",
        "IC": "IC",
        "CR": "CR",
        "RT": "RT",
        "IR": "IR",
        "CT": "CT",
        # fallbacks to the primary mechanism in case of ties that don’t match pairs
        "I": "IR",  # Mirror as a reflective I
        "C": "CT",  # Swiss Knife as operational C
        "R": "RT",  # Milo Tin as transformative R
        "T": "IT",  # Lego Synth as integrative T
    }
    if pair in mapping:
        return mapping[pair]
    return mapping.get(primary, "ALL")

def underused(scores):
    # Return mechanisms sorted by ascending score (lowest first)
    return sorted(scores.items(), key=lambda x: x[1])[:2]

def bar_chart(scores):
    cats = ["Identification (I)", "Coordination (C)", "Reflection (R)", "Transformation (T)"]
    vals = [scores["I"], scores["C"], scores["R"], scores["T"]]
    fig = go.Figure(go.Bar(
        x=vals, y=cats, orientation="h",
        marker=dict(color=["#2471A3", "#17A589", "#F1C40F", "#8E44AD"])
    ))
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10),
                      xaxis_title="Selections", yaxis_title="")
    return fig

def scenario_ui(index):
    sc = SCENARIOS[index]
    st.markdown(f"### {sc['title']}")
    st.caption(sc["context"])
    with st.expander("Why this is tricky", expanded=False):
        st.write(sc["why"])
    options = [label for (label, _m) in sc["opts"]]
    prev = st.session_state.answers.get(index, None)
    default = options.index(prev) if prev in options else None
    choice = st.radio("What would you most likely do?", options, index=default, label_visibility="collapsed", key=f"q_{index}")
    cols = st.columns(2)
    back = cols[0].button("◀ Back", disabled=(st.session_state.page == 0), use_container_width=True, key=f"b_{index}")
    nxt  = cols[1].button("Next ▶", use_container_width=True, key=f"n_{index}")

    if back:
        st.session_state.page -= 1
        st.rerun()
    if nxt:
        if choice is None:
            st.warning("Please choose an option to continue.")
        else:
            st.session_state.answers[index] = choice
            st.session_state.page += 1
            st.rerun()

def results_ui():
    scores = score_mechanisms()
    st.success("🌊 You’ve completed your Boundary Compass journey.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("I", scores["I"]); m2.metric("C", scores["C"]); m3.metric("R", scores["R"]); m4.metric("T", scores["T"])
    st.plotly_chart(bar_chart(scores), use_container_width=True)

    code = pick_archetype(scores)
    name, desc = ARCHETYPES[code]
    st.markdown(f"## {name}")
    st.write(desc)

    # Strength narrative
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dom = [ordered[0][0], ordered[1][0]]
    dom_text = " and ".join({"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}[d] for d in dom)
    st.markdown(f"**Your current pattern:** You tend to begin boundary work through *{dom_text}*.")

    # Stretch narrative
    low_two = underused(scores)
    st.markdown("**Your next edge:**")
    for mech, _val in low_two:
        label = {"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}[mech]
        st.write(f"- *{label}*: {MICRO_PRACTICES[mech]}")

    st.divider()
    st.caption(FOOTER)

# ------------------------------------------------------------
# App flow
# ------------------------------------------------------------
init_state()

st.title(TITLE)
st.caption(SUB)

with st.expander("What is this about?", expanded=False):
    st.markdown(INTRO)

progress = st.session_state.page / len(SCENARIOS)
st.progress(progress)

if st.session_state.page < len(SCENARIOS):
    idx = st.session_state.order[st.session_state.page]
    scenario_ui(idx)
else:
    results_ui()