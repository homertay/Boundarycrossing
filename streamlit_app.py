import random
import streamlit as st
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG + LIGHT CSS
# ============================================================
st.set_page_config(page_title="The Boundary Compass", page_icon="🧭", layout="centered")

def apply_css():
    st.markdown("""
    <style>
      .stApp { background: linear-gradient(180deg, #F7FBFF 0%, #FFFFFF 60%); }
      .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 900px; }
      details { border-radius: 12px; background: #ffffff; border: 1px solid #ebeff3; }
      .stRadio > div { gap: 0.75rem; }
      .stRadio label {
        background: #ffffff; border: 1px solid #e5ecf3; border-radius: 12px;
        padding: 0.9rem 1rem; width: 100%; transition: all .12s ease;
      }
      .stRadio label:hover { border-color: #c3d5ea; background: #f9fcff; }
      #MainMenu, header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

TITLE = "🧭 The Boundary Compass — Singapore / ASEAN Workplace Edition"
SUB = "See your default move in complexity — and what else could work"

INTRO = """
In complex work, the toughest moments live **at the boundaries** — between roles, functions, values, and systems.

This game reflects how you tend to cross boundaries using four mechanisms:
**Identification (I)** – clarifying purpose & differences  
**Coordination (C)** – building shared routines or tools  
**Reflection (R)** – making sense through dialogue  
**Transformation (T)** – turning insights into new practices

Pick what you would **most likely** do.  
After each choice, take a quick **reflection nudge** — then move on.
"""

FOOTER = "*Inspired by boundary-crossing research (Akkerman & Bakker, 2011).*"
MECH_COLORS = {"I": (36,113,163), "C": (23,165,137), "R": (241,196,15), "T": (142,68,173)}

# ============================================================
# 12 RICH, WORKPLACE-DRIVEN SCENARIOS (SG/ASEAN, MID–SENIOR)
# Each offers first-person responses that map to I/C/R/T
# ============================================================
SCENARIOS = [
    {
        "key": "s1",
        "title": "Global Template, Local Reality (Banking / ASEAN)",
        "context": (
            "HQ insists every market uses the same compliance template. Vietnam and Indonesia teams say some fields don’t fit local rules. "
            "Risk wants consistency; country heads want flexibility; delivery is slipping."
        ),
        "why": "Boundary: global standard vs. local adaptation.",
        "opts": [
            ("I’ll draw a clear line: which fields are non-negotiable, which can be localised.", "I"),
            ("I’ll co-create a single checklist mapping local differences to the global form.", "C"),
            ("I’ll ask HQ privately what reputational fear is driving uniformity — what would build trust?", "R"),
            ("I’ll pilot a 'local-within-global' version in one market and share outcomes.", "T"),
        ],
    },
    {
        "key": "s2",
        "title": "Innovation Under Governance (GLC / Singapore)",
        "context": (
            "Your CEO says 'innovate like a start-up' while new ideas still pass three committees. "
            "Your team is sceptical — they’ve seen proposals die in process."
        ),
        "why": "Boundary: aspiration vs. system.",
        "opts": [
            ("I’ll clarify where experimentation is truly authorised and what remains governed.", "I"),
            ("I’ll design a fast-track lane: small budget, lighter approvals, clear guardrails.", "C"),
            ("I’ll check with committee heads what 'risk' actually means to them.", "R"),
            ("I’ll run one sprint, document what governance helped or hindered, and propose tweaks.", "T"),
        ],
    },
    {
        "key": "s3",
        "title": "Regional Call, Different Rhythms (ASEAN)",
        "context": (
            "On a tri-country call (SG/Jakarta/Bangkok), direct voices dominate early; concerns surface late via side-chats. "
            "Deadlines slip because issues stay unspoken until the end."
        ),
        "why": "Boundary: efficiency vs. inclusion; directness vs. respect.",
        "opts": [
            ("I’ll name the pattern and define who decides, who speaks, and who follows up.", "I"),
            ("I’ll rotate facilitation and use a live notes doc where all add points.", "C"),
            ("I’ll ask each market what silence or disagreement signals in their culture.", "R"),
            ("I’ll co-design a new cadence (round-robins, pre-reads) and trial for a month.", "T"),
        ],
    },
    {
        "key": "s4",
        "title": "Net-Zero vs. Margin (Manufacturing / Board)",
        "context": (
            "Sustainability wants plant retrofits; Finance warns margins will dip; the board wants both credibility and returns. "
            "Investors are asking for a plan."
        ),
        "why": "Boundary: purpose and performance.",
        "opts": [
            ("I’ll define what 'material impact' means for the board and investors.", "I"),
            ("I’ll convene Finance, Ops, ESG to build a shared cost/benefit model.", "C"),
            ("I’ll host a dialogue on the firm’s appetite for reputational vs. financial risk.", "R"),
            ("I’ll propose one-plant retrofit as a learning pilot with milestones.", "T"),
        ],
    },
    {
        "key": "s5",
        "title": "Office Days or Real Culture? (Hybrid / Singapore)",
        "context": (
            "Policy says three days in office. Productivity is fine, but cohesion feels weaker; leaders claim 'culture can’t happen on Zoom.' "
            "Teams want autonomy; the company wants community."
        ),
        "why": "Boundary: flexibility vs. belonging.",
        "opts": [
            ("I’ll clarify what culture outcomes are expected from office time.", "I"),
            ("I’ll align on team-specific rhythms instead of a blanket rule.", "C"),
            ("I’ll ask staff which moments actually build connection and why.", "R"),
            ("I’ll design hybrid rituals that recreate those moments (online/offline).", "T"),
        ],
    },
    {
        "key": "s6",
        "title": "Founder Gravity (Family Business / ASEAN)",
        "context": (
            "You’re the first non-family COO. The founder still signs major decisions; the next generation wants change but avoids conflict. "
            "You need progress without rupture."
        ),
        "why": "Boundary: legacy vs. renewal.",
        "opts": [
            ("I’ll define which decisions require founder sign-off and which can be delegated.", "I"),
            ("I’ll institute a weekly steering meeting with both generations and fixed agenda.", "C"),
            ("I’ll explore with each side what 'losing control' or 'earning trust' means.", "R"),
            ("I’ll build a dual-sign-off model for one unit and show effect on speed/quality.", "T"),
        ],
    },
    {
        "key": "s7",
        "title": "Calibration Bias (Multicultural Team / Appraisals)",
        "context": (
            "In calibration, confident self-promoters are rewarded; modest high-performers get overlooked. "
            "You sense style is outshining substance."
        ),
        "why": "Boundary: cultural humility vs. visibility; fairness through equity, not equality.",
        "opts": [
            ("I’ll clarify evaluation criteria and evidence expectations up front.", "I"),
            ("I’ll coach quieter staff to prepare impact stories and data.", "C"),
            ("I’ll reflect with HR on biases for presentation over contribution.", "R"),
            ("I’ll revise templates to weight collaboration and stewardship.", "T"),
        ],
    },
    {
        "key": "s8",
        "title": "Digital Roadmap, Again (Transformation / Org)",
        "context": (
            "It’s the third 'digital roadmap' in five years. Managers joke the decks change faster than systems. "
            "A new CDO asks you to 're-energise the ground.'"
        ),
        "why": "Boundary: messaging vs. meaning; theatre vs. lived change.",
        "opts": [
            ("I’ll list what has actually changed vs. what’s rebranded.", "I"),
            ("I’ll co-create small, visible wins near customers and measure adoption.", "C"),
            ("I’ll ask teams why previous efforts lost traction; listen for patterns.", "R"),
            ("I’ll launch one real workflow change and publish before/after metrics.", "T"),
        ],
    },
    {
        "key": "s9",
        "title": "Vendor Velocity vs. Compliance Brakes (Tech / Regulated)",
        "context": (
            "Overseas vendor sprints fast; your compliance team checks everything thoroughly. "
            "Releases keep slipping; both sides are frustrated."
        ),
        "why": "Boundary: agility vs. safety.",
        "opts": [
            ("I’ll define what counts as 'critical risk' for both sides.", "I"),
            ("I’ll set a shared release cadence with clear checkpoints.", "C"),
            ("I’ll host a retrospective on where each side felt blocked and why.", "R"),
            ("I’ll prototype a hybrid sprint model combining both rhythms.", "T"),
        ],
    },
    {
        "key": "s10",
        "title": "Public-Sector Partnership (Private x Agency)",
        "context": (
            "Your firm co-delivers with a government agency. You value speed; they value consensus. "
            "Timelines slip; both say 'different ways of working.'"
        ),
        "why": "Boundary: agility vs. legitimacy; fast results vs. due process.",
        "opts": [
            ("I’ll clarify which deliverables are time-sensitive vs. which need formal sign-offs.", "I"),
            ("I’ll map approval gates together and agree turnaround times.", "C"),
            ("I’ll reflect jointly on fears: loss of reputation vs. loss of relevance.", "R"),
            ("I’ll run a co-delivery pilot with delegated authority and review impact.", "T"),
        ],
    },
    {
        "key": "s11",
        "title": "Newly Acquired, Not Assimilated (M&A / Region)",
        "context": (
            "Your SG company acquired a Thai SME. HQ pushes quick integration; Thai team fears losing identity. "
            "Emails are polite; tension is real."
        ),
        "why": "Boundary: identity vs. efficiency — integrate without assimilation.",
        "opts": [
            ("I’ll name non-negotiables (brand, reporting, safety) vs. areas for localisation.", "I"),
            ("I’ll create mixed working groups to harmonise policy step by step.", "C"),
            ("I’ll host listening sessions on what 'being part of the group' means locally.", "R"),
            ("I’ll design a joint-brand product to honour both names and test together.", "T"),
        ],
    },
    {
        "key": "s12",
        "title": "The Retention Puzzle (Post-Covid / Purpose)",
        "context": (
            "Top performers leave for start-ups offering flexibility and purpose. "
            "The board wants a retention plan; you know money alone won’t fix it."
        ),
        "why": "Boundary: extrinsic vs. intrinsic motivation; reward vs. meaning.",
        "opts": [
            ("I’ll clarify our true value proposition beyond pay.", "I"),
            ("I’ll involve employees in shaping career paths and flexibility norms.", "C"),
            ("I’ll run dialogues: what keeps you here, what might make you leave?", "R"),
            ("I’ll prototype a talent-experience initiative centred on purpose stories and impact.", "T"),
        ],
    },
]

# ============================================================
# REFLECTION NUDGES (after each choice)
# ============================================================
NUDGES = {
    "I": "You chose **Identification** — clarity reduces noise. Notice when stating isn’t enough without **testing** something small.",
    "C": "You chose **Coordination** — structure helps flow. Watch if process becomes protection from **trying**.",
    "R": "You chose **Reflection** — sense-making opens learning. Beware staying in analysis instead of **acting**.",
    "T": "You chose **Transformation** — experiments shift systems. Check that new patterns still honour core **boundaries**.",
}

# ============================================================
# MICRO-PRACTICES (concrete next steps)
# ============================================================
MICRO_PRACTICES = {
    "I": "Run a 15-min **kick-off clarity** huddle before your next project. Pin a 1-page note: purpose, roles, decision rights, out-of-scope.",
    "C": "Create **one shared artefact** this week (checklist, template, or dashboard) that two functions agree to use.",
    "R": "After a key meeting, host a 5-min **sense-making pause**: ‘What did we learn? What assumptions surfaced?’ Capture one line each.",
    "T": "Pick one cross-team pain point and run a **1-week mini-experiment** (new handover, short sync, or co-lead trial). If it works, bake it in.",
}

# ============================================================
# STATE & SCORING
# ============================================================
def init_state():
    if "order" not in st.session_state:
        st.session_state.order = list(range(len(SCENARIOS)))
        random.shuffle(st.session_state.order)
    if "page" not in st.session_state:
        st.session_state.page = 0           # which scenario (0..11)
    if "answers" not in st.session_state:
        st.session_state.answers = {i: None for i in range(len(SCENARIOS))}
    if "subpage" not in st.session_state:
        st.session_state.subpage = 0        # 0=question, 1=reflection

def score_mechanisms():
    s = {"I":0, "C":0, "R":0, "T":0}
    for i, a in st.session_state.answers.items():
        if a:
            for (opt, m) in SCENARIOS[i]["opts"]:
                if a == opt: s[m] += 1
    return s

def top_mechanisms(scores, k=2):
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [m for m,_ in ordered[:k]]

def underused(scores, k=2):
    ordered = sorted(scores.items(), key=lambda x: x[1])
    return [m for m,_ in ordered[:k]]

# ============================================================
# UI — SCENARIO + REFLECTION NUDGE + RESULTS
# ============================================================
def scenario_ui(i):
    sc = SCENARIOS[i]
    if st.session_state.subpage == 0:
        # QUESTION
        st.markdown(f"### {sc['title']}")
        st.caption(sc["context"])
        with st.expander("Why this matters", expanded=False):
            st.write(sc["why"])

        options = [o for (o,_m) in sc["opts"]]
        prev = st.session_state.answers.get(i)
        default = options.index(prev) if prev in options else 0
        choice = st.radio("Your most likely move?", options, index=default,
                          label_visibility="collapsed", key=f"q_{i}")

        c1, c2 = st.columns(2)
        if c1.button("◀ Back", disabled=(st.session_state.page == 0), use_container_width=True):
            st.session_state.page -= 1
            st.session_state.subpage = 0
            st.rerun()
        if c2.button("Next ▶", use_container_width=True):
            st.session_state.answers[i] = choice
            st.session_state.subpage = 1
            st.rerun()
    else:
        # REFLECTION NUDGE
        picked = st.session_state.answers[i]
        mech = None
        for (opt, m) in SCENARIOS[i]["opts"]:
            if opt == picked:
                mech = m
                break

        st.info(f"**You chose:** {picked}")
        st.markdown("### Quick reflection")
        st.write(NUDGES.get(mech, "Notice what this opens — and what it might miss."))
        st.markdown("> If this were you: *What could be true here that you haven’t considered?*")

        if st.button("Continue ▶", use_container_width=True):
            st.session_state.subpage = 0
            st.session_state.page += 1
            st.rerun()

def results_ui():
    scores = score_mechanisms()
    st.success("🎉 You’ve completed your Boundary Compass")

    # Metrics + bar chart
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("I", scores["I"]); c2.metric("C", scores["C"]); c3.metric("R", scores["R"]); c4.metric("T", scores["T"])

    fig = go.Figure(go.Bar(
        x=[scores["I"], scores["C"], scores["R"], scores["T"]],
        y=["Identification (I)", "Coordination (C)", "Reflection (R)", "Transformation (T)"],
        orientation="h",
        marker=dict(color=[MECH_COLORS[k] for k in ["I","C","R","T"]])
    ))
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

    # Pattern summary
    names = {"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}
    top2 = top_mechanisms(scores, 2)
    st.markdown(f"**Where you tend to start:** *{', '.join(names[m] for m in top2)}*")

    # Stretch prompts
    lows = underused(scores, 2)
    st.markdown("**Try this next week (small, practical):**")
    for m in lows:
        st.write(f"- **{names[m]}** — {MICRO_PRACTICES[m]}")

    st.divider()
    st.write("**One small reflection:** Which upcoming situation might test your Compass — and what tiny experiment will you try?")
    st.caption(FOOTER)

# ============================================================
# APP FLOW
# ============================================================
def main():
    apply_css()
    init_state()

    st.title(TITLE)
    st.caption(SUB)
    with st.expander("What this is", expanded=False):
        st.markdown(INTRO)

    progress = (st.session_state.page + st.session_state.subpage * 0.5) / len(SCENARIOS)
    st.progress(progress)

    if st.session_state.page < len(SCENARIOS):
        idx = st.session_state.order[st.session_state.page]
        scenario_ui(idx)
    else:
        results_ui()

if __name__ == "__main__":
    main()