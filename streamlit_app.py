import streamlit as st
import plotly.graph_objects as go
import random

# ------------------------------------------------------------
# App configuration
# ------------------------------------------------------------
st.set_page_config(page_title="The Boundary Compass", page_icon="🧭", layout="centered")

TITLE = "🧭 The Boundary Compass — Singapore Workplace Edition"
SUB = "A short reflective game on how you show up at boundaries: Identification · Coordination · Reflection · Transformation"

INTRO = """
In complex work, the toughest moments live **at the boundaries** — between roles, functions, values, and systems.

This game helps you notice your **preferred way of crossing boundaries**, based on four learning mechanisms
(Akkerman & Bakker, 2011):

- **Identification (I)** — seeing and naming differences & purpose clearly  
- **Coordination (C)** — building shared routines, tools, agreements  
- **Reflection (R)** — making sense across perspectives through dialogue  
- **Transformation (T)** — prototyping hybrid practices and embedding change

Choose what you would **most likely** do in each situation.  
At the end, you’ll see your **Boundary Compass** profile, an archetype, and stretch prompts.
"""

FOOTER = "*Mechanisms adapted from boundary-crossing research (Akkerman & Bakker, 2011).*"

# ------------------------------------------------------------
# 12 short, role-neutral Singapore workplace scenarios
# ------------------------------------------------------------
SCENARIOS = [
    {
        "key": "s1",
        "title": "The Idea That Lands Flat",
        "context": "You share an idea in a meeting that you think could help. No one reacts. The silence is awkward.",
        "why": "You could withdraw, push harder, or try a different way to engage. How do you respond?",
        "opts": [
            ("Clarify the problem you were trying to solve and restate your intent.", "I"),
            ("Ask for quick feedback or invite others to build on it together.", "C"),
            ("Pause and reflect: what might make others hesitant to respond?", "R"),
            ("Prototype your idea quietly and share results later.", "T"),
        ],
    },
    {
        "key": "s2",
        "title": "The Overloaded Team",
        "context": "Your team has been running on full capacity, and a new project drops in unexpectedly.",
        "why": "People are tired, but the work matters. You have to decide how to move forward.",
        "opts": [
            ("Clarify what’s truly essential and what can wait.", "I"),
            ("Re-prioritise tasks together and agree on timelines.", "C"),
            ("Ask how everyone is coping and what support they need.", "R"),
            ("Propose a new rhythm or workflow to make work more sustainable.", "T"),
        ],
    },
    {
        "key": "s3",
        "title": "The Quiet Colleague",
        "context": "A capable teammate rarely speaks up during discussions, even when you know they have good ideas.",
        "why": "You sense a missed opportunity for learning and inclusion.",
        "opts": [
            ("Check in privately to understand their comfort level.", "I"),
            ("Create smaller group discussions where everyone contributes.", "C"),
            ("Reflect on what dynamics might silence some voices.", "R"),
            ("Invite them to co-lead a small task to build confidence.", "T"),
        ],
    },
    {
        "key": "s4",
        "title": "The Missing Context",
        "context": "You’re added to a project halfway through. Goals and decisions are unclear, but deadlines are close.",
        "why": "You could act fast, or slow down to orient yourself.",
        "opts": [
            ("Ask for clarity on purpose, roles, and current status.", "I"),
            ("Set up a short sync to align everyone quickly.", "C"),
            ("Observe for a bit to understand group patterns.", "R"),
            ("Sketch a quick summary of what’s known and test it with the group.", "T"),
        ],
    },
    {
        "key": "s5",
        "title": "The Tech Shortcut",
        "context": "A new AI tool could save hours of manual work, but no one has tested it yet.",
        "why": "You sense potential, but also the risk of wasting time if it fails.",
        "opts": [
            ("Clarify what success looks like before adopting the tool.", "I"),
            ("Run a short trial with clear check-in points.", "C"),
            ("Ask why people hesitate and what concerns they have.", "R"),
            ("Test it on one process and share what you learn.", "T"),
        ],
    },
    {
        "key": "s6",
        "title": "The Feedback Moment",
        "context": "A peer asks, “Be honest — how was my presentation?” You saw both strengths and gaps.",
        "why": "It’s a chance to help, but you’re unsure how direct to be.",
        "opts": [
            ("Ask what kind of feedback they’d find most useful first.", "I"),
            ("Use a simple framework to share both positives and improvements.", "C"),
            ("Reflect on why giving feedback feels tricky for you.", "R"),
            ("Offer to practise together before their next presentation.", "T"),
        ],
    },
    {
        "key": "s7",
        "title": "The Sticky Stakeholder",
        "context": "A senior stakeholder keeps changing direction. The team’s energy is fading.",
        "why": "You could comply, challenge, or help the system make sense of itself.",
        "opts": [
            ("Clarify expectations and what success means this round.", "I"),
            ("Summarise changes and confirm decisions in writing.", "C"),
            ("Explore why priorities keep shifting — what pressures exist upstream?", "R"),
            ("Co-create a shared decision tracker or playbook for future projects.", "T"),
        ],
    },
    {
        "key": "s8",
        "title": "The Missed Deadline",
        "context": "A deliverable slips, affecting others. You weren’t solely at fault, but you were part of it.",
        "why": "It’s a test of accountability and learning culture.",
        "opts": [
            ("Acknowledge the miss and clarify your part.", "I"),
            ("Meet quickly with affected teams to reset timelines.", "C"),
            ("Ask what blind spots or assumptions contributed.", "R"),
            ("Share lessons learnt and suggest how to avoid repeats.", "T"),
        ],
    },
    {
        "key": "s9",
        "title": "The Team Debate",
        "context": "Two teammates strongly disagree on an approach — one wants structure, the other prefers experimentation.",
        "why": "Both have valid points. You’re caught in the middle.",
        "opts": [
            ("Clarify what problem we’re really solving before choosing.", "I"),
            ("Agree on next steps: try one approach with review points.", "C"),
            ("Ask each to explain the principle behind their view.", "R"),
            ("Combine both ideas into a short pilot to test outcomes.", "T"),
        ],
    },
    {
        "key": "s10",
        "title": "The Change Rollout",
        "context": "A new policy launches and complaints flood in: “Another change again?”",
        "why": "Change fatigue is real, but the change matters.",
        "opts": [
            ("Clarify what the change fixes and what stays the same.", "I"),
            ("Create a quick Q&A resource and feedback loop.", "C"),
            ("Ask what worries people most about new changes.", "R"),
            ("Turn early feedback into tweaks that show responsiveness.", "T"),
        ],
    },
    {
        "key": "s11",
        "title": "The Sustainability Trade-Off",
        "context": "Your company wants to go greener, but sustainable materials slow production and raise costs.",
        "why": "Short-term targets clash with long-term commitments.",
        "opts": [
            ("Define what 'sustainability' really means in this context.", "I"),
            ("Bring Finance, Ops, and Sustainability together to review trade-offs.", "C"),
            ("Hold a dialogue on what 'responsible growth' means for the team.", "R"),
            ("Pilot a lower-impact process and measure both cost and learning.", "T"),
        ],
    },
    {
        "key": "s12",
        "title": "The Small Win",
        "context": "The team just completed a tough sprint. Everyone rushes to the next task.",
        "why": "Celebration feels like a luxury, but reflection builds capability.",
        "opts": [
            ("Acknowledge what went well and who made it happen.", "I"),
            ("Create a five-minute retrospective at the next stand-up.", "C"),
            ("Ask what surprised or challenged people most.", "R"),
            ("Turn insights into a new team ritual for learning and gratitude.", "T"),
        ],
    },
]

# ------------------------------------------------------------
# Archetypes (SG-flavoured) + stretch micro-practices
# ------------------------------------------------------------
ARCHETYPES = {
    "IT": ("🧩 Lego Synthesiser", "You integrate old and new wisely, re-assembling pieces into better forms."),
    "IC": ("🎫 EZ-Link Navigator", "You read systems quickly and help people move through rules and structures."),
    "CR": ("🧂 Condiment Connector", "You blend people and process; things go smoother when you’re around."),
    "RT": ("🥫 Milo Tin Transformer", "You learn fast and repurpose experience into creative new practice."),
    "IR": ("🪞 Kopitiam Mirror", "You surface assumptions and help others see clearly — with care and calm."),
    "CT": ("🧰 Swiss Knife Collaborator", "You make innovation operational — bridging ideas into routines."),
    "ALL": ("🌀 Boundary Alchemist", "You flex across all four mechanisms and catalyse learning in others."),
    "LOW": ("🪑 The Settler", "You stabilise the space; with gentle stretch you’ll expand your range."),
}

MICRO_PRACTICES = {
    "I": "Before the next project, write a one-page 'boundary brief': purpose, roles, red lines, decision rights.",
    "C": "Create one simple boundary object (checklist, glossary, or ritual) that others can re-use.",
    "R": "Run a 20-minute sense-making huddle: What surprised us? What assumptions surfaced?",
    "T": "Prototype one small hybrid change; embed it as a repeatable routine if it works.",
}

# ------------------------------------------------------------
# State & helpers
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
        return "ALL"
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary, secondary = ordered[0][0], ordered[1][0]
    pair = primary + secondary
    mapping = {
        "IT": "IT", "IC": "IC", "CR": "CR", "RT": "RT", "IR": "IR", "CT": "CT",
        "I": "IR", "C": "CT", "R": "RT", "T": "IT"
    }
    if pair in mapping:
        return mapping[pair]
    return mapping.get(primary, "ALL")

def underused(scores):
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

# ------------------------------------------------------------
# UI
# ------------------------------------------------------------
def scenario_ui(index: int):
    sc = SCENARIOS[index]
    st.markdown(f"### {sc['title']}")
    st.caption(sc["context"])
    with st.expander("Why this matters", expanded=False):
        st.write(sc["why"])

    options = [label for (label, _m) in sc["opts"]]
    prev = st.session_state.answers.get(index, None)
    default = options.index(prev) if prev in options else 0  # mobile-friendly default
    choice = st.radio("What would you most likely do?",
                      options, index=default, label_visibility="collapsed", key=f"q_{index}")

    c1, c2 = st.columns(2)
    back = c1.button("◀ Back", disabled=(st.session_state.page == 0), use_container_width=True, key=f"b_{index}")
    nxt  = c2.button("Next ▶", use_container_width=True, key=f"n_{index}")

    if back:
        st.session_state.page -= 1
        st.rerun()
    if nxt:
        st.session_state.answers[index] = choice
        st.session_state.page += 1
        st.rerun()

def results_ui():
    scores = score_mechanisms()
    st.success("🎉 You’ve completed your Boundary Compass journey.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("I", scores["I"]); c2.metric("C", scores["C"]); c3.metric("R", scores["R"]); c4.metric("T", scores["T"])
    st.plotly_chart(bar_chart(scores), use_container_width=True)

    code = pick_archetype(scores)
    name, desc = ARCHETYPES[code]
    st.markdown(f"## {name}")
    st.write(desc)

    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dom = [ordered[0][0], ordered[1][0]]
    dom_text = " and ".join({"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}[d] for d in dom)
    st.markdown(f"**Your pattern:** You tend to begin boundary work through *{dom_text}*.")

    st.markdown("**Your next edge:**")
    for mech, _val in underused(scores):
        label = {"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}[mech]
        st.write(f"- *{label}*: {MICRO_PRACTICES[mech]}")

    st.divider()
    st.markdown("**One small reflection for the week:** Which upcoming situation might test your Compass — and what tiny experiment will you try?")
    st.caption(FOOTER)

# ------------------------------------------------------------
# App flow
# ------------------------------------------------------------
init_state()

st.title(TITLE)
st.caption(SUB)
with st.expander("What is this about?", expanded=False):
    st.markdown(INTRO)

st.progress(st.session_state.page / len(SCENARIOS))

if st.session_state.page < len(SCENARIOS):
    idx = st.session_state.order[st.session_state.page]
    scenario_ui(idx)
else:
    results_ui()