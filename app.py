"""
MBX Boundary Crossing Diagnostic — SJT Edition
Master in Boundary-Crossing Learning and Leadership | IAL/SUSS

Design:
  • 20 situational judgement scenarios (4 dimensions × 5 organisational levels)
  • Each scenario has 4 developmentally-ordered response options (scored 1–4)
  • Levels: Systemic, Team, Leader–Subordinate, Individual Mindset, Technology
  • Scoring: sum of 5 scenario responses per dimension (max 20)
  • Google Sheets via Apps Script webhook (set GOOGLE_SHEET_URL in st.secrets)
  • Facilitator dashboard + HTML report download
"""

import random
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Boundary Crossing Diagnostic | MBX",
    page_icon="🔀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

FACILITATOR_PASSWORD = "mbx2026"

# ─────────────────────────────────────────────────────────────────────────────
# GOOGLE SHEETS SUBMISSION
# Submit via a Google Apps Script web app URL stored in st.secrets
# Setup instructions shown in facilitator sidebar
# ─────────────────────────────────────────────────────────────────────────────
def submit_to_sheets(row: dict) -> bool:
    try:
        url = st.secrets.get("GOOGLE_SHEET_URL", "")
        if not url:
            return False
        r = requests.post(url, json=row, timeout=8)
        return r.status_code == 200
    except Exception:
        return False

# ─────────────────────────────────────────────────────────────────────────────
# SHARED CLASS STORE (in-memory for facilitator dashboard live view)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_class_store():
    return []

# ─────────────────────────────────────────────────────────────────────────────
# DIMENSION METADATA
# ─────────────────────────────────────────────────────────────────────────────
DIMENSIONS = {
    "awareness": {
        "name": "Boundary Awareness",
        "icon": "🔍",
        "color": "#2563EB",
        "tagline": "Noticing and naming the limits of your practice",
        "feedback": [
            "You tend to treat boundary signals as task problems rather than relational or structural ones. Building the habit of pausing to name 'what kind of problem is this?' can open up more options.",
            "You notice boundaries in familiar situations. The next step is developing confidence to name them explicitly — even when doing so creates discomfort in the room.",
            "You have a well-developed capacity to identify and articulate boundaries. Consider how you might help others develop this awareness as part of your leadership practice.",
            "You are not just noticing boundaries — you are surfacing them as collective learning opportunities. This is a rare and high-value leadership capability.",
        ],
    },
    "coordination": {
        "name": "Coordination",
        "icon": "🤝",
        "color": "#10B981",
        "tagline": "Building bridges, shared routines, and lasting structures",
        "feedback": [
            "You tend to rely on informal coordination — relationships, goodwill, and individual effort. These work until they don't. Building lightweight shared structures can make your team's work more resilient.",
            "You create coordination fixes when things break down. The shift to designing coordination proactively — before problems surface — can significantly reduce friction.",
            "You build effective coordination structures and help others work through shared systems. Ensure the structures you create are owned by the team, not dependent on you.",
            "You design coordination as infrastructure — systems and norms that outlast any individual and create the conditions for sustained cross-boundary collaboration.",
        ],
    },
    "reflection": {
        "name": "Reflective Capacity",
        "icon": "🪞",
        "color": "#F59E0B",
        "tagline": "Learning about yourself through encounters with difference",
        "feedback": [
            "Boundary encounters are data about your assumptions — but only if you examine them. Starting a simple reflective practice (even a few lines after a difficult meeting) can significantly deepen your self-awareness.",
            "You reflect when prompted or when something goes wrong. Building regular reflection into your rhythm — not just reactive — will help you extract more learning from your experiences.",
            "You use encounters with difference as genuine learning material. Your willingness to sit with discomfort and examine your assumptions is a significant leadership strength.",
            "You treat your own reactions as data, share reflections with others, and create conditions for collective sense-making. This is transformative reflective leadership.",
        ],
    },
    "transformation": {
        "name": "Transformative Practice",
        "icon": "✨",
        "color": "#8B5CF6",
        "tagline": "Generating new knowledge and practice through crossing",
        "feedback": [
            "Your boundary crossings may not yet be generating new practice. Consider: what could be done differently if you treated this tension as a design opportunity rather than a problem to manage?",
            "You occasionally generate new insights from boundary work. Look for opportunities to turn these into deliberate pilots — small, safe experiments with clear learning goals.",
            "You actively create conditions for new practice to emerge. You know how to scope experiments, involve others, and document learning in ways that can travel.",
            "You are not just crossing boundaries — you are transforming practices on both sides. You treat every significant boundary encounter as a potential site of institutional learning.",
        ],
    },
}

LEVEL_LABELS = {
    "systemic": "🏛 Systemic",
    "team": "👥 Team",
    "leader_sub": "🧑‍💼 Leader–Subordinate",
    "mindset": "🧠 Individual Mindset",
    "technology": "💻 Technology",
}

# ─────────────────────────────────────────────────────────────────────────────
# 20 SJT SCENARIOS
# Each option scored 1 (Emerging) → 4 (Advanced) on that dimension
# ─────────────────────────────────────────────────────────────────────────────
SCENARIOS = [
    # ── BOUNDARY AWARENESS ──────────────────────────────────────────────────
    {
        "id": "A1", "dim": "awareness", "level": "systemic",
        "title": "Two Worlds, One Meeting",
        "context": (
            "Your agency is undergoing restructuring. Two divisions that used to operate independently "
            "are now expected to collaborate on service delivery. Staff attend joint meetings but seem "
            "to be talking past each other — using the same words to mean very different things. "
            "You are the middle manager bridging both teams."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Focus on getting tasks done — alignment will happen naturally as people work together.", 1),
            ("Notice the confusion but assume it will resolve once roles become clearer post-restructuring.", 2),
            ("Name the pattern explicitly in a meeting: 'I think we're using the same words but meaning different things — let's surface that.'", 3),
            ("Document the specific gaps, facilitate a joint glossary session, and flag this as a structural issue for HR/OD to address.", 4),
        ],
    },
    {
        "id": "A2", "dim": "awareness", "level": "team",
        "title": "The Same Words, Different Maps",
        "context": (
            "Your project team includes members from three departments. During planning, you notice "
            "that what 'stakeholder engagement' means to each person varies significantly — "
            "one thinks it means informing, another means consulting, a third means co-designing. "
            "The difference hasn't been named aloud."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Proceed with planning — everyone is experienced and will figure out what's needed as they go.", 1),
            ("Notice the variation but don't raise it, hoping the team lead will address it.", 2),
            ("Pause planning and ask each person to describe what good stakeholder engagement looks like from their experience.", 3),
            ("Facilitate a short boundary-mapping exercise to surface the different mental models and use this as a design input for the engagement strategy.", 4),
        ],
    },
    {
        "id": "A3", "dim": "awareness", "level": "leader_sub",
        "title": "Missing the Unspoken",
        "context": (
            "A junior officer consistently delivers work that meets the technical brief but misses "
            "the political sensitivities you consider obvious. When you give feedback, they seem confused — "
            "they thought they had done exactly what was asked."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Be more explicit in your briefs — the gap is about communication clarity, not boundaries.", 1),
            ("Notice there is a gap in how you each see the work but assume it's just a matter of experience over time.", 2),
            ("Have a direct conversation about the unspoken expectations you carry, naming what has been implicit in your instructions.", 3),
            ("Treat this as a boundary moment — explicitly discuss the different mental models you each bring and co-create a shared checklist of considerations.", 4),
        ],
    },
    {
        "id": "A4", "dim": "awareness", "level": "mindset",
        "title": "The Irritation Signal",
        "context": (
            "You notice you feel irritated when a colleague from another division challenges your team's "
            "approach in a joint meeting. Later, reflecting privately, you wonder if the irritation "
            "is about something deeper than the content of their challenge."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Let the feeling pass — it was a minor moment and doesn't warrant further attention.", 1),
            ("Acknowledge privately that you may have been defensive, but move on without exploring further.", 2),
            ("Spend time examining what exactly triggered the reaction, and whether it reveals an assumption you hold about your team's work.", 3),
            ("Use the experience as data — journal about it, discuss with a trusted peer, and consider how it might be shaping your leadership decisions.", 4),
        ],
    },
    {
        "id": "A5", "dim": "awareness", "level": "technology",
        "title": "The Tool You Keep Overriding",
        "context": (
            "Your division adopted an AI-assisted analysis tool six months ago. You notice that the "
            "tool consistently flags issues your team would not have caught, but your team tends to "
            "dismiss its outputs as 'not applicable to our context' without detailed examination."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Let the team decide whether to use the tool — they know the operational context best.", 1),
            ("Encourage the team to try the tool more but don't push if they are resistant.", 2),
            ("Name the pattern: 'I notice we're consistently overriding the tool's outputs — let's examine when that's a genuine contextual judgment and when it might be habit.'", 3),
            ("Facilitate a structured review of three cases where the tool was overridden, asking the team to articulate their reasoning — using this to surface hidden assumptions about expertise and AI.", 4),
        ],
    },

    # ── COORDINATION ─────────────────────────────────────────────────────────
    {
        "id": "C1", "dim": "coordination", "level": "systemic",
        "title": "Waiting for the Other Side",
        "context": (
            "Two departments must jointly deliver a new citizen-facing service. Each has its own "
            "approval processes, reporting timelines, and internal KPIs. The project keeps stalling "
            "because each side waits for the other to 'go first' on key decisions."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Escalate to your director and ask for clearer ownership to be assigned from above.", 1),
            ("Arrange a meeting between the two department heads to sort out who does what.", 2),
            ("Design a simple shared RACI matrix and joint milestone tracker that both teams agree to work from.", 3),
            ("Co-design a lightweight governance structure — shared decision rights, escalation paths, and a joint review cadence — and propose it as a model for future cross-agency collaboration.", 4),
        ],
    },
    {
        "id": "C2", "dim": "coordination", "level": "team",
        "title": "The Meeting That Goes Nowhere",
        "context": (
            "Your team's weekly update meetings are increasingly unproductive. Some people give "
            "long status updates; others stay silent. Important decisions get deferred week after week. "
            "Team members are politely disengaged but nobody has said anything directly."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Keep the format — it is familiar and any change might create resistance or signal criticism.", 1),
            ("Shorten the meetings and send a pre-read template to try to improve efficiency.", 2),
            ("Redesign the meeting structure with the team — separating information-sharing (async), decision-making (synchronous), and relationship-building (informal).", 3),
            ("Facilitate a team conversation about what coordination actually requires in your current context, co-design new formats, and build in a quarterly review of team norms.", 4),
        ],
    },
    {
        "id": "C3", "dim": "coordination", "level": "leader_sub",
        "title": "Knowledge in Your Head",
        "context": (
            "You manage a team where important context, relationships, and institutional knowledge "
            "live in your head and in informal conversations with one or two trusted officers. "
            "Newer or quieter team members are regularly left out. When you're away, things slow down."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Keep the current arrangement — it works well enough and formal systems create overhead.", 1),
            ("Start CC-ing more people on key emails to improve information flow.", 2),
            ("Create a shared team knowledge base and set expectations that key decisions and context are documented in it.", 3),
            ("Redesign how knowledge flows in your team — map what information exists where, who needs it, and co-design lightweight systems that outlast any individual's tenure.", 4),
        ],
    },
    {
        "id": "C4", "dim": "coordination", "level": "mindset",
        "title": "The Relationship-Based Coordinator",
        "context": (
            "You prefer to coordinate through relationships — you rely on knowing the right people "
            "and calling in favours. This has served you well. But you notice it creates bottlenecks "
            "when you're unavailable, and newer staff cannot replicate your approach."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Continue as is — relationship-based coordination is a core leadership skill that cannot be systematised.", 1),
            ("Brief a deputy so they can cover the most important relationships when you are absent.", 2),
            ("Reflect on which coordination tasks rely solely on your relationships and begin building shared processes to replace them.", 3),
            ("Treat this as a leadership development moment — map your relational capital, create handover systems, and actively coach team members to build their own cross-boundary relationships.", 4),
        ],
    },
    {
        "id": "C5", "dim": "coordination", "level": "technology",
        "title": "Four Tools, No Rules",
        "context": (
            "Your team uses at least four different platforms (email, Teams, shared drives, a project tracker) "
            "with no agreed norms. The same information exists in multiple places. "
            "People use different tools for the same tasks. Coordination friction is high."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Let individuals use whichever tools they prefer — flexibility is important and people resist change.", 1),
            ("Suggest the team standardise on one or two tools but leave implementation to each manager.", 2),
            ("Facilitate a team audit of current tool usage and co-design a simple technology charter: which tool for which purpose.", 3),
            ("Design a team coordination architecture — map the workflows, identify friction points, co-select tools with the team, and build in a quarterly review as needs evolve.", 4),
        ],
    },

    # ── REFLECTIVE CAPACITY ──────────────────────────────────────────────────
    {
        "id": "R1", "dim": "reflection", "level": "systemic",
        "title": "Between Loyalty and Responsibility",
        "context": (
            "A new policy is introduced that you are expected to implement. You have serious reservations "
            "about its unintended consequences for frontline staff, but the policy has been signed off at a "
            "senior level. You feel caught between institutional loyalty and responsibility to your team."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Implement the policy as directed — it is not your role to second-guess senior leadership decisions.", 1),
            ("Note your reservations privately, implement the policy, and monitor for issues.", 2),
            ("Implement the policy while raising your concerns through appropriate channels, documenting your perspective and the evidence you observe.", 3),
            ("Facilitate a team conversation about how to implement with integrity, surface the assumptions in the policy design, and contribute structured feedback to the policy review process.", 4),
        ],
    },
    {
        "id": "R2", "dim": "reflection", "level": "team",
        "title": "The Feedback You Didn't Expect",
        "context": (
            "After a difficult team project, several team members give informal feedback that they found "
            "your leadership style in meetings controlling. You were not aware of this at all — "
            "your intention had been simply to keep the team focused under pressure."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Note the feedback but put it down to personality differences — you know what works in high-pressure situations.", 1),
            ("Reflect privately and decide to be less prescriptive in future meetings.", 2),
            ("Follow up with the team members who gave feedback, ask for specific examples, and share your own perspective on what you were trying to do.", 3),
            ("Create a structured team debrief — share what you heard, own your impact, explore the gap between intention and experience, and co-design meeting norms going forward.", 4),
        ],
    },
    {
        "id": "R3", "dim": "reflection", "level": "leader_sub",
        "title": "What the Exit Revealed",
        "context": (
            "A high-performing officer leaves your team for a lateral move. In the exit conversation, "
            "they mention they felt they weren't growing — that you kept giving them work they were "
            "already good at rather than stretching them. This surprises you."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Accept the feedback graciously and note it for future reference.", 1),
            ("Reflect on whether you unconsciously relied on this person too much and try to be more deliberate with future high performers.", 2),
            ("Sit with the discomfort of the feedback — examine your assumptions about what development looks like and whether you were prioritising team stability over individual growth.", 3),
            ("Use this as a catalyst for a genuine review of your development practice — have conversations with remaining team members about their growth needs and examine your own defaults around stretch versus safety.", 4),
        ],
    },
    {
        "id": "R4", "dim": "reflection", "level": "mindset",
        "title": "When You Should Have Spoken",
        "context": (
            "You notice that in cross-agency meetings, you consistently defer to the most senior "
            "person in the room even when you have directly relevant expertise. Afterwards, you "
            "often think: 'I should have said something.' This pattern has repeated for months."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Attribute this to appropriate professional deference — hierarchy matters and you respect that.", 1),
            ("Acknowledge the pattern to yourself but assume it's just your personality and hard to change.", 2),
            ("Examine the assumptions driving the pattern — what are you afraid of, and when does deference serve the work versus when does it undermine it?", 3),
            ("Treat this as a leadership edge — work with a coach or mentor on the roots of the pattern, practise speaking up in lower-stakes situations, and develop a personal strategy for managing deference and voice.", 4),
        ],
    },
    {
        "id": "R5", "dim": "reflection", "level": "technology",
        "title": "Who Is Writing This Report?",
        "context": (
            "Your team has been using an AI tool for drafting reports. You notice the outputs are "
            "being accepted with minimal review. When you ask why, team members say the AI 'sounds "
            "more polished.' You feel a vague professional unease but are not sure exactly why."
        ),
        "prompt": "What do you do?",
        "options": [
            ("As long as the reports are accurate and well-written, the process doesn't matter.", 1),
            ("Mention to the team that they should review outputs carefully, but don't explore the unease further.", 2),
            ("Name your unease explicitly and facilitate a team conversation about what professional judgment and accountability mean in an AI-assisted workflow.", 3),
            ("Facilitate a deeper team inquiry — what does authorship mean when AI is involved? What are the ethical and professional implications? Develop a team position and working norms.", 4),
        ],
    },

    # ── TRANSFORMATIVE PRACTICE ──────────────────────────────────────────────
    {
        "id": "T1", "dim": "transformation", "level": "systemic",
        "title": "The Task Force That Changes Nothing",
        "context": (
            "After years of siloed working, your organisation has created a formal cross-agency task force. "
            "You are the manager representative. Despite good intentions, the task force produces reports "
            "that neither agency acts on. The structure exists but generates no change."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Continue participating — institutional change at this level takes time and persistence.", 1),
            ("Raise the issue at the next meeting and suggest a review of the task force's mandate.", 2),
            ("Propose a redesign — shift from reporting to joint prototyping. Identify one concrete shared problem and design a small cross-team experiment.", 3),
            ("Facilitate a fundamental rethink of the task force's purpose — from compliance structure to learning engine — with new governance, success metrics, and a mandate to surface systemic insights to leadership.", 4),
        ],
    },
    {
        "id": "T2", "dim": "transformation", "level": "team",
        "title": "The Practice Only Your Team Knows",
        "context": (
            "Your team has developed a genuinely better way of running citizen consultations — "
            "co-designing with community members rather than presenting options for feedback. "
            "It is working well. But the practice lives only within your team."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Continue the practice within your team — it's not your role to advocate for others to change.", 1),
            ("Mention it to peers informally and let interest develop organically.", 2),
            ("Document the approach and share it with your director, proposing a pilot in one other team.", 3),
            ("Treat this as a boundary object — create a shareable, adaptable version of the methodology, run a cross-team learning session, and propose it as input to the agency's service design framework.", 4),
        ],
    },
    {
        "id": "T3", "dim": "transformation", "level": "leader_sub",
        "title": "The Unconventional Proposal",
        "context": (
            "A junior officer proposes an unconventional approach to a persistent operational problem. "
            "The idea is outside standard procedure but technically feasible. "
            "Your instinct is that senior management will not approve it."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Thank them for the idea and redirect them to focus on the current approved approach.", 1),
            ("Explore the idea informally with them but be honest that approval seems unlikely.", 2),
            ("Work with them to develop a low-risk pilot proposal — scoped small enough to test the idea without requiring full approval.", 3),
            ("Treat this as a leadership development opportunity — co-develop the proposal, coach them through the political landscape, create conditions for a genuine pilot, and document learnings regardless of outcome.", 4),
        ],
    },
    {
        "id": "T4", "dim": "transformation", "level": "mindset",
        "title": "The Expert Who Must Now Facilitate",
        "context": (
            "You have always been most effective in an expert role — giving clear direction, "
            "holding high standards, being the person with the answer. You're now in a context "
            "that requires more facilitation, ambiguity tolerance, and distributed leadership. "
            "You find the shift genuinely uncomfortable."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Continue leading from expertise — it's what you're good at and what the team expects from you.", 1),
            ("Try facilitative approaches in some meetings while defaulting to direction when pressure is high.", 2),
            ("Name the shift explicitly with yourself and your team — experiment deliberately with facilitative approaches and reflect on what you're learning about your leadership range.", 3),
            ("Treat this discomfort as a developmental signal — design a sustained personal experiment with a reflective practice (journalling, peer coaching, supervision) to support genuine transformation in how you lead.", 4),
        ],
    },
    {
        "id": "T5", "dim": "transformation", "level": "technology",
        "title": "Not Just Automating — Reimagining",
        "context": (
            "You've been exploring AI tools with your team. You've identified a core workflow "
            "that could be fundamentally redesigned around AI capabilities — not just automating "
            "existing steps, but genuinely rethinking how the work gets done. "
            "The potential is real but the change is significant."
        ),
        "prompt": "What do you do?",
        "options": [
            ("Proceed carefully and incrementally — significant workflow changes carry risk and require approval.", 1),
            ("Discuss the idea with your team and gauge interest before deciding whether to pursue it.", 2),
            ("Design a structured pilot — define the workflow, set learning metrics, run a 4-week experiment with a small group, and report findings.", 3),
            ("Co-create genuinely new practice with your team — involve them in the design, surface their mental models about work and AI, and build a shared learning architecture that can scale and inform others.", 4),
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────────────────────────────────────
def compute_scores(answers: dict) -> dict:
    totals = {k: 0 for k in DIMENSIONS}
    for sc in SCENARIOS:
        chosen_score = answers.get(sc["id"])
        if chosen_score is not None:
            totals[sc["dim"]] += chosen_score
    return totals

def score_tier(s: float, max_s: float = 20):
    pct = s / max_s
    if pct < 0.40:  return "Emerging",   "#F97316", 0
    if pct < 0.60:  return "Developing", "#3B82F6", 1
    if pct < 0.80:  return "Proficient", "#10B981", 2
    return               "Advanced",   "#8B5CF6", 3

# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────
def make_radar(all_scores: list, labels: list, title="Boundary Crossing Profile"):
    dim_keys  = list(DIMENSIONS.keys())
    dim_names = [DIMENSIONS[k]["name"] for k in dim_keys]
    palette   = ["#2563EB", "#F59E0B", "#10B981", "#8B5CF6", "#EF4444"]
    fig = go.Figure()
    for i, scores in enumerate(all_scores):
        vals  = [scores[k] for k in dim_keys] + [scores[dim_keys[0]]]
        theta = dim_names + [dim_names[0]]
        c     = palette[i % len(palette)]
        r,g,b = int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=theta, fill="toself",
            fillcolor=f"rgba({r},{g},{b},0.12)",
            line=dict(color=c, width=2.5),
            name=labels[i],
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(248,250,252,0.9)",
            radialaxis=dict(
                visible=True, range=[0, 20],
                tickvals=[5, 10, 15, 20],
                tickfont=dict(size=10, color="#94A3B8"),
                gridcolor="rgba(148,163,184,0.25)",
                linecolor="rgba(148,163,184,0.25)",
            ),
            angularaxis=dict(
                gridcolor="rgba(148,163,184,0.2)",
                tickfont=dict(size=12, color="#334155"),
            ),
        ),
        showlegend=len(all_scores) > 1,
        legend=dict(font=dict(size=11)),
        title=dict(text=title, font=dict(size=14, color="#1E293B", family="Georgia,serif"), x=0.5),
        paper_bgcolor="white", plot_bgcolor="white",
        height=400, margin=dict(t=65, b=10, l=20, r=20),
    )
    return fig

def make_bar(scores):
    keys   = list(DIMENSIONS.keys())
    colors = [DIMENSIONS[k]["color"] for k in keys]
    names  = [f"{DIMENSIONS[k]['icon']} {DIMENSIONS[k]['name']}" for k in keys]
    vals   = [scores[k] for k in keys]
    fig = go.Figure(go.Bar(
        x=vals, y=names, orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{v}/20" for v in vals],
        textposition="outside",
        textfont=dict(size=12, color="#1E293B"),
    ))
    fig.update_layout(
        height=240,
        xaxis=dict(range=[0, 24], showgrid=True, gridcolor="#E2E8F0",
                   tickfont=dict(color="#94A3B8", size=10), zeroline=False),
        yaxis=dict(tickfont=dict(size=12, color="#334155")),
        paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(t=10, b=10, l=10, r=50),
        showlegend=False,
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# HTML REPORT
# ─────────────────────────────────────────────────────────────────────────────
def html_report(name, scores, class_code=""):
    now  = datetime.now().strftime("%d %B %Y")
    meta = name
    if class_code: meta += f" · {class_code}"
    meta += f" · {now}"

    rows = ""
    for key, dim in DIMENSIONS.items():
        s          = scores[key]
        label, lc, tidx = score_tier(s)
        pct        = (s / 20) * 100
        feedback   = dim["feedback"][tidx]
        rows += f"""
        <div style="background:white;border-radius:12px;padding:1.2rem 1.5rem;margin-bottom:1rem;
                    border-left:5px solid {dim['color']};box-shadow:0 2px 8px rgba(0,0,0,0.07)">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
            <span style="font-weight:700;font-size:1rem">{dim['icon']} {dim['name']}</span>
            <span style="background:{lc};color:white;padding:3px 12px;border-radius:999px;
                         font-size:0.73rem;font-weight:700">{label.upper()}</span>
          </div>
          <div style="font-size:0.78rem;color:#94A3B8;font-style:italic;margin-bottom:8px">{dim['tagline']}</div>
          <div style="font-size:1.9rem;font-weight:800;color:#1E293B;font-family:Georgia,serif;margin-bottom:6px">
            {s}<span style="font-size:1rem;font-weight:400;color:#94A3B8"> / 20</span></div>
          <div style="background:#E2E8F0;border-radius:999px;height:7px;margin-bottom:10px">
            <div style="background:{dim['color']};width:{pct:.0f}%;height:7px;border-radius:999px"></div></div>
          <p style="margin:0;font-size:0.88rem;color:#475569;line-height:1.7">{feedback}</p>
        </div>"""

    # Level breakdown hint
    level_rows = ""
    for sc in SCENARIOS:
        ans = ""  # not stored in report for privacy
        level_rows += ""

    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boundary Crossing Diagnostic — {name}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;700&family=DM+Sans:wght@400;500;600&display=swap');
  body {{ font-family:'DM Sans',sans-serif; max-width:680px; margin:40px auto;
          padding:0 24px; color:#1E293B; background:#F8FAFC; }}
  .header {{ background:linear-gradient(135deg,#0F172A,#1E3A8A,#2563EB);
             border-radius:16px; padding:2.2rem 2rem; color:white; margin-bottom:1.5rem; }}
  .header .label {{ font-size:0.62rem; letter-spacing:3px; text-transform:uppercase; opacity:0.6; margin-bottom:0.6rem; }}
  .header h1 {{ margin:0; font-size:1.7rem; font-family:'Lora',Georgia,serif; font-weight:700; }}
  .header .meta {{ margin:8px 0 0; opacity:0.8; font-size:0.88rem; }}
  .section {{ font-family:'Lora',Georgia,serif; font-size:1.15rem; color:#1E293B; margin:1.5rem 0 0.75rem; }}
  .reflect {{ background:#EFF6FF; border-left:4px solid #2563EB; border-radius:8px;
              padding:1.1rem 1.3rem; margin:1.25rem 0; }}
  .reflect h3 {{ margin:0 0 0.5rem; color:#1D4ED8; font-size:0.88rem; text-transform:uppercase; letter-spacing:1px; }}
  .reflect p {{ margin:0; color:#475569; font-size:0.9rem; line-height:1.7; font-style:italic; }}
  .footer {{ text-align:center; font-size:0.78rem; color:#CBD5E1; margin-top:2rem;
             padding-top:1rem; border-top:1px solid #E2E8F0; }}
</style></head><body>
  <div class="header">
    <div class="label">MBX · Master in Boundary-Crossing Learning and Leadership · IAL/SUSS</div>
    <h1>🔀 Boundary Crossing Diagnostic</h1>
    <div class="meta">{meta}</div>
  </div>
  <p style="color:#475569;font-size:0.9rem;line-height:1.75;margin-bottom:1.25rem">
    This diagnostic is based on your responses to 20 situational scenarios across five organisational levels: 
    systemic, team, leader–subordinate, individual mindset, and technology. 
    Scores reflect developmental tendencies, not fixed traits.
  </p>
  <p class="section">Dimension Scores</p>
  {rows}
  <div class="reflect">
    <h3>💭 Reflection Prompt</h3>
    <p>Which dimension surprised you most — either higher or lower than expected? 
    What does the gap between your highest and lowest dimension tell you about where 
    your leadership energy is currently focused? 
    What is one specific scenario type where you want to lead differently?</p>
  </div>
  <div class="footer">MBX Boundary Crossing Diagnostic · IAL/SUSS · {now}<br>
    Inspired by Akkerman &amp; Bakker (2011) boundary-crossing theory.</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
def apply_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"] { font-family:'DM Sans',sans-serif; }
.main { background:#F8FAFC; }
.block-container { padding-top:1.5rem !important; max-width:720px !important; padding-bottom:3rem !important; }
#MainMenu,header,footer { visibility:hidden; }

.hero {
    background:linear-gradient(135deg,#0F172A 0%,#1E3A8A 55%,#2563EB 100%);
    border-radius:18px; padding:2.6rem 2.2rem; color:white;
    margin-bottom:1.5rem; text-align:center; position:relative; overflow:hidden;
}
.hero::before {
    content:''; position:absolute; top:-60%; right:-15%;
    width:320px; height:320px; background:rgba(255,255,255,0.03); border-radius:50%;
}
.hero-label { font-size:0.62rem; letter-spacing:3px; text-transform:uppercase; opacity:0.6; margin-bottom:0.8rem; }
.hero h1 { font-family:'Lora',Georgia,serif; font-size:2rem; font-weight:700; margin:0; line-height:1.2; }
.hero p { font-size:0.92rem; opacity:0.8; margin:0.85rem auto 0; line-height:1.65; max-width:500px; }

.card {
    background:white; border-radius:14px; padding:1.3rem 1.5rem;
    margin-bottom:1rem; box-shadow:0 1px 6px rgba(15,23,42,0.07);
    border:1px solid rgba(226,232,240,0.8);
}
.sc-level { font-size:0.72rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
            color:#94A3B8; margin-bottom:0.4rem; }
.sc-title { font-family:'Lora',Georgia,serif; font-size:1.1rem; font-weight:700; color:#1E293B; margin-bottom:0.5rem; }
.sc-context { font-size:0.91rem; color:#475569; line-height:1.75; }
.sc-prompt { font-size:0.85rem; font-weight:600; color:#1E293B; margin:0.75rem 0 0.5rem; }

.prog-wrap { margin-bottom:1.25rem; }
.prog-label { display:flex; justify-content:space-between; font-size:0.78rem; color:#64748B; margin-bottom:5px; }
.prog-bg { background:#E2E8F0; border-radius:999px; height:5px; }
.prog-fill { height:5px; border-radius:999px; background:linear-gradient(90deg,#1E40AF,#3B82F6); }

.r-card {
    background:white; border-radius:14px; padding:1.2rem 1.5rem;
    margin-bottom:0.85rem; box-shadow:0 2px 8px rgba(15,23,42,0.07);
    border:1px solid rgba(226,232,240,0.8);
}
.r-header { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem; }
.r-name { font-weight:700; font-size:1rem; color:#1E293B; }
.r-tagline { font-size:0.78rem; color:#94A3B8; margin-top:3px; font-style:italic; }
.r-badge { color:white; padding:3px 12px; border-radius:999px; font-size:0.71rem; font-weight:700; letter-spacing:0.5px; white-space:nowrap; }
.r-score { font-family:'Lora',Georgia,serif; font-size:2rem; font-weight:700; color:#1E293B; margin-bottom:5px; line-height:1; }
.r-score span { font-family:'DM Sans',sans-serif; font-size:1rem; font-weight:400; color:#94A3B8; }
.r-bar-bg { background:#E2E8F0; border-radius:999px; height:6px; margin-bottom:0.85rem; }
.r-bar-fill { height:6px; border-radius:999px; }
.r-text { font-size:0.88rem; color:#475569; line-height:1.75; margin:0; }

.level-pills { display:flex; gap:0.4rem; flex-wrap:wrap; margin-bottom:0.85rem; }
.pill { background:#F1F5F9; border-radius:6px; padding:3px 10px;
        font-size:0.72rem; font-weight:600; color:#475569; }
.pill.best { background:#D1FAE5; color:#065F46; }
.pill.low  { background:#FEF3C7; color:#92400E; }

.reflect-box {
    background:#EFF6FF; border-left:4px solid #2563EB; border-radius:10px;
    padding:1.1rem 1.4rem; margin:1.25rem 0;
}
.reflect-title { font-weight:700; color:#1D4ED8; font-size:0.85rem; margin-bottom:0.5rem; }
.reflect-text { font-size:0.9rem; color:#475569; line-height:1.75; margin:0; font-style:italic; }

.confirm-box {
    background:linear-gradient(135deg,#064E3B,#059669);
    border-radius:14px; padding:1.5rem 2rem; color:white; text-align:center; margin:1rem 0;
}
.confirm-box h3 { margin:0 0 0.4rem; font-size:1.1rem; }
.confirm-box p { margin:0; opacity:0.85; font-size:0.88rem; }

.stButton > button {
    background:linear-gradient(135deg,#1E3A8A,#2563EB) !important;
    color:white !important; border:none !important; border-radius:10px !important;
    padding:0.62rem 1.5rem !important; font-weight:600 !important; font-size:0.93rem !important;
    width:100% !important; font-family:'DM Sans',sans-serif !important; transition:all 0.2s !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 18px rgba(37,99,235,0.3) !important; }

div[data-testid="stRadio"] > label { display:none !important; }
div[data-testid="stRadio"] div[role="radiogroup"] { flex-direction:column !important; gap:0.5rem !important; }
div[data-testid="stRadio"] div[role="radiogroup"] label {
    background:#F8FAFC; border-radius:10px; padding:0.75rem 1rem !important;
    font-size:0.9rem !important; color:#334155 !important;
    border:1.5px solid #E2E8F0; transition:all 0.15s; cursor:pointer; width:100%;
}
div[data-testid="stRadio"] div[role="radiogroup"] label:hover { background:#EFF6FF; border-color:#93C5FD; }
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
    background:#EFF6FF; border-color:#2563EB; color:#1D4ED8 !important; font-weight:600;
}
.stTextInput > div > div > input {
    border-radius:10px !important; border:1.5px solid #E2E8F0 !important;
    font-family:'DM Sans',sans-serif !important; font-size:0.95rem !important;
    padding:0.6rem 1rem !important; background:white !important;
}
.stTextInput > div > div > input:focus { border-color:#2563EB !important; box-shadow:0 0 0 3px rgba(37,99,235,0.1) !important; }
section[data-testid="stSidebar"] { background:#0F172A !important; }
section[data-testid="stSidebar"] * { color:white !important; }
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    background:rgba(255,255,255,0.1) !important; border-color:rgba(255,255,255,0.2) !important; color:white !important;
}
details { border-radius:10px !important; background:white !important; border:1px solid #E2E8F0 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "welcome", "q_idx": 0, "order": None,
        "answers": {}, "name": "", "class_code": "",
        "submitted": False, "fac_mode": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
def facilitator_sidebar():
    with st.sidebar:
        st.markdown("### 🔒 Facilitator Access")
        pw = st.text_input("Password", type="password", key="fac_pw", label_visibility="collapsed")
        if st.button("Enter Facilitator View"):
            if pw == FACILITATOR_PASSWORD:
                st.session_state.fac_mode = True
                st.rerun()
            else:
                st.error("Incorrect password")
        if st.session_state.fac_mode:
            st.success("✅ Facilitator mode active")
            if st.button("Exit"):
                st.session_state.fac_mode = False
                st.rerun()
            st.markdown("---")
            store = get_class_store()
            if store and st.button("🗑 Clear In-Memory Results"):
                store.clear()
                st.rerun()
            st.markdown("---")
            st.markdown("**📋 Google Sheets Setup**")
            st.markdown("""
1. Create a Google Sheet  
2. Extensions → Apps Script → paste this code and deploy as web app (Anyone):

```javascript
function doPost(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheets()[0];
  var d  = JSON.parse(e.postData.contents);
  if (sh.getLastRow() === 0) {
    sh.appendRow(Object.keys(d));
  }
  sh.appendRow(Object.values(d));
  return ContentService.createTextOutput("ok");
}
```

3. Copy the web app URL  
4. In Streamlit Cloud → app Settings → Secrets, add:

```
GOOGLE_SHEET_URL = "https://script.google.com/..."
```
""")

# ─────────────────────────────────────────────────────────────────────────────
# FACILITATOR DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
def show_facilitator():
    store = get_class_store()
    st.markdown("""
    <div class="hero" style="text-align:left;padding:1.8rem 2rem">
      <div class="hero-label">Facilitator Dashboard · MBX</div>
      <h1 style="font-size:1.5rem">🎓 Class Results</h1>
    </div>""", unsafe_allow_html=True)

    if not store:
        st.info("📭 No submissions yet. Participants click 'Submit to Class' after completing the diagnostic.")
        return

    st.metric("Participants submitted", len(store))
    dim_keys  = list(DIMENSIONS.keys())
    all_s     = [r["scores"] for r in store]
    avg       = {k: round(sum(s[k] for s in all_s) / len(all_s), 1) for k in dim_keys}

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_radar([avg], ["Class Average"], "Class Average"), use_container_width=True)
    with col2:
        labels = [r["name"].split()[0] for r in store]
        st.plotly_chart(make_radar(all_s, labels, "All Participants"), use_container_width=True)

    st.markdown("#### Individual Scores")
    rows = []
    for r in store:
        row = {"Name": r["name"], "Time": r["timestamp"]}
        for k in dim_keys:
            row[DIMENSIONS[k]["name"]] = f"{r['scores'][k]}/20"
        row["Class Code"] = r.get("class_code", "—")
        rows.append(row)
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("📥 Download CSV", data=df.to_csv(index=False),
                       file_name=f"mbx_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                       mime="text/csv")

    st.markdown("---")
    st.markdown("#### 💬 Debrief Starters")
    sorted_dims = sorted(dim_keys, key=lambda k: avg[k])
    low_d = DIMENSIONS[sorted_dims[0]]
    hi_d  = DIMENSIONS[sorted_dims[-1]]
    st.markdown(f"""
    <div style="background:#F0FDF4;border-left:4px solid #10B981;border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.75rem">
      <strong>Collective strength: {hi_d['icon']} {hi_d['name']} ({avg[sorted_dims[-1]]:.1f}/20)</strong><br>
      <span style="font-size:0.9rem;color:#475569">What conditions in your organisations have cultivated this capacity? 
      Where does it create blind spots?</span>
    </div>
    <div style="background:#FFF7ED;border-left:4px solid #F59E0B;border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.75rem">
      <strong>Collective growth edge: {low_d['icon']} {low_d['name']} ({avg[sorted_dims[0]]:.1f}/20)</strong><br>
      <span style="font-size:0.9rem;color:#475569">Which organisational level (systemic, team, leader–subordinate, 
      mindset, technology) feels hardest for this dimension — and why?</span>
    </div>
    <div style="background:#EFF6FF;border-left:4px solid #2563EB;border-radius:10px;padding:1rem 1.2rem">
      <strong>Scenario that landed hardest</strong><br>
      <span style="font-size:0.9rem;color:#475569">Which of the 20 scenarios felt most uncomfortably real? 
      What does that tell us about the boundaries in our current roles?</span>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# WELCOME
# ─────────────────────────────────────────────────────────────────────────────
def show_welcome():
    st.markdown("""
    <div class="hero">
      <div class="hero-label">MBX · IAL/SUSS · Supporting Development</div>
      <div style="font-size:3rem;margin-bottom:0.6rem">🔀</div>
      <h1>Boundary Crossing Diagnostic</h1>
      <p>20 real workplace scenarios across five organisational levels — 
      surface where your boundary-crossing leadership is strong, and where it wants to grow.</p>
    </div>""", unsafe_allow_html=True)

    with st.expander("ℹ️ About this tool", expanded=False):
        st.markdown("""
This diagnostic uses **situational judgement scenarios** drawn from real Singapore workplace tensions. 
Rather than rating abstract statements about yourself, you respond to concrete situations — 
which reveals more about your actual boundary-crossing tendencies.

**Four dimensions** are assessed across **five organisational levels**:

| Dimension | What it measures |
|---|---|
| 🔍 **Boundary Awareness** | Noticing and naming the invisible lines that shape your work |
| 🤝 **Coordination** | Building shared structures, routines, and bridging artefacts |
| 🪞 **Reflective Capacity** | Learning about yourself through encounters with difference |
| ✨ **Transformative Practice** | Generating new knowledge and practice through crossing |

**Five levels:** Systemic · Team · Leader–Subordinate · Individual Mindset · Technology

Each scenario has four response options on a developmental continuum.  
Choose what you would **most likely do** — not the ideal answer.

*Inspired by Akkerman & Bakker (2011) boundary-crossing theory.*
""")

    name_val = st.text_input("Your name", value=st.session_state.name,
                              placeholder="e.g. Wei Lin", label_visibility="visible")
    code_val = st.text_input("Class code (from your facilitator)",
                              value=st.session_state.class_code,
                              placeholder="e.g. MBX-APR2026", label_visibility="visible")

    st.markdown("""
    <div style="display:flex;gap:0.75rem;margin:1rem 0;flex-wrap:wrap">
      <div style="background:white;border-radius:10px;padding:0.7rem 1rem;flex:1;min-width:100px;
                  box-shadow:0 1px 4px rgba(0,0,0,0.07);text-align:center;border:1px solid #E2E8F0">
        <div style="font-size:1.3rem;margin-bottom:2px">📋</div>
        <div style="font-size:0.75rem;font-weight:600;color:#475569">20 scenarios</div>
      </div>
      <div style="background:white;border-radius:10px;padding:0.7rem 1rem;flex:1;min-width:100px;
                  box-shadow:0 1px 4px rgba(0,0,0,0.07);text-align:center;border:1px solid #E2E8F0">
        <div style="font-size:1.3rem;margin-bottom:2px">⏱</div>
        <div style="font-size:0.75rem;font-weight:600;color:#475569">~15 minutes</div>
      </div>
      <div style="background:white;border-radius:10px;padding:0.7rem 1rem;flex:1;min-width:100px;
                  box-shadow:0 1px 4px rgba(0,0,0,0.07);text-align:center;border:1px solid #E2E8F0">
        <div style="font-size:1.3rem;margin-bottom:2px">🏛👥🧑‍💼🧠💻</div>
        <div style="font-size:0.75rem;font-weight:600;color:#475569">5 org levels</div>
      </div>
      <div style="background:white;border-radius:10px;padding:0.7rem 1rem;flex:1;min-width:100px;
                  box-shadow:0 1px 4px rgba(0,0,0,0.07);text-align:center;border:1px solid #E2E8F0">
        <div style="font-size:1.3rem;margin-bottom:2px">📄</div>
        <div style="font-size:0.75rem;font-weight:600;color:#475569">PDF report</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if st.button("Begin Diagnostic →"):
        if not name_val.strip():
            st.warning("Please enter your name to continue.")
        else:
            st.session_state.name       = name_val.strip()
            st.session_state.class_code = code_val.strip()
            order = list(range(len(SCENARIOS)))
            random.shuffle(order)
            st.session_state.order   = order
            st.session_state.answers = {}
            st.session_state.q_idx   = 0
            st.session_state.page    = "quiz"
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# QUIZ
# ─────────────────────────────────────────────────────────────────────────────
def show_quiz():
    idx   = st.session_state.q_idx
    total = len(SCENARIOS)
    sc    = SCENARIOS[st.session_state.order[idx]]
    dim   = DIMENSIONS[sc["dim"]]
    level_label = LEVEL_LABELS[sc["level"]]

    pct = idx / total
    st.markdown(f"""
    <div class="prog-wrap">
      <div class="prog-label">
        <span>Scenario {idx + 1} of {total}</span>
        <span style="color:{dim['color']};font-weight:600">{dim['icon']} {dim['name']}</span>
      </div>
      <div class="prog-bg"><div class="prog-fill" style="width:{pct*100:.0f}%"></div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
      <div class="sc-level">{level_label}</div>
      <div class="sc-title">{sc['title']}</div>
      <p class="sc-context">{sc['context']}</p>
      <p class="sc-prompt">{sc['prompt']}</p>
    </div>""", unsafe_allow_html=True)

    opts    = [o for (o, _) in sc["options"]]
    scores  = [s for (_, s) in sc["options"]]
    prev_score = st.session_state.answers.get(sc["id"])
    prev_opt   = opts[scores.index(prev_score)] if prev_score in scores else None
    default    = opts.index(prev_opt) if prev_opt in opts else 0

    choice = st.radio("", opts, index=default, key=f"q_{sc['id']}")

    is_last = idx == total - 1
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", disabled=(idx == 0)):
            chosen_score = scores[opts.index(choice)]
            st.session_state.answers[sc["id"]] = chosen_score
            st.session_state.q_idx -= 1
            st.rerun()
    with col2:
        btn_label = "See My Results →" if is_last else "Next →"
        if st.button(btn_label):
            chosen_score = scores[opts.index(choice)]
            st.session_state.answers[sc["id"]] = chosen_score
            if is_last:
                st.session_state.page = "results"
            else:
                st.session_state.q_idx += 1
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────────────────────────────────
def show_results():
    scores = compute_scores(st.session_state.answers)
    name   = st.session_state.name

    st.markdown(f"""
    <div class="hero" style="padding:2rem 2.2rem;text-align:left">
      <div class="hero-label">Your Profile · MBX / IAL-SUSS</div>
      <h1 style="font-size:1.5rem">🔀 Boundary Crossing Profile</h1>
      <p style="margin:6px 0 0;font-size:0.88rem">{name}</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_radar([scores], [name]), use_container_width=True)
    with col2:
        st.plotly_chart(make_bar(scores), use_container_width=True)

    # Per-dimension level breakdown
    level_scores = {}
    for sc in SCENARIOS:
        ans = st.session_state.answers.get(sc["id"], 0)
        key = (sc["dim"], sc["level"])
        level_scores[key] = ans

    st.markdown("<h3 style='font-family:Lora,Georgia,serif;color:#1E293B;margin-bottom:0.75rem'>"
                "Dimension Profiles</h3>", unsafe_allow_html=True)

    for key, dim in DIMENSIONS.items():
        s = scores[key]
        label, lc, tidx = score_tier(s)
        pct = (s / 20) * 100
        feedback = dim["feedback"][tidx]

        # Level breakdown pills
        level_pill_html = "<div class='level-pills'>"
        dim_levels = [(lv, level_scores.get((key, lv), 0)) for lv in LEVEL_LABELS]
        sorted_levels = sorted(dim_levels, key=lambda x: x[1], reverse=True)
        for i, (lv, lv_score) in enumerate(sorted_levels):
            cls = "pill best" if i == 0 else ("pill low" if i == len(sorted_levels)-1 else "pill")
            level_pill_html += f"<span class='{cls}'>{LEVEL_LABELS[lv]} {lv_score}/4</span>"
        level_pill_html += "</div>"

        st.markdown(f"""
        <div class="r-card" style="border-left:5px solid {dim['color']}">
          <div class="r-header">
            <div>
              <div class="r-name">{dim['icon']} {dim['name']}</div>
              <div class="r-tagline">{dim['tagline']}</div>
            </div>
            <span class="r-badge" style="background:{lc}">{label.upper()}</span>
          </div>
          <div class="r-score">{s}<span> / 20</span></div>
          <div class="r-bar-bg">
            <div class="r-bar-fill" style="background:{dim['color']};width:{pct:.0f}%"></div>
          </div>
          {level_pill_html}
          <p class="r-text">{feedback}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="reflect-box">
      <div class="reflect-title">💭 Reflection Prompt</div>
      <p class="reflect-text">
        Which dimension surprised you — higher or lower than expected? 
        Look at the level pills on your lowest dimension: which organisational level 
        (systemic, team, leader–subordinate, mindset, technology) scored lowest? 
        What does that tell you about where boundary-crossing feels hardest in your current role?
      </p>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    report = html_report(name, scores, st.session_state.class_code)
    st.download_button(
        "📄 Download My Report (open → Print → Save as PDF)",
        data=report,
        file_name=f"BC_Diagnostic_{name.replace(' ','_')}.html",
        mime="text/html",
        use_container_width=True,
    )

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    if not st.session_state.submitted:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:#1E293B;margin-bottom:0.4rem">📤 Submit to Class & Research Dataset</div>
          <p style="margin:0;font-size:0.87rem;color:#475569;line-height:1.65">
            Share your dimension scores with the facilitator's live dashboard and the research dataset 
            (Google Sheets). Only your name and four scores are shared — your individual scenario 
            responses remain private.
          </p>
        </div>""", unsafe_allow_html=True)
        if st.button("✅ Submit to Class"):
            store = get_class_store()
            row = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "name": name,
                "class_code": st.session_state.class_code,
                "awareness": scores["awareness"],
                "coordination": scores["coordination"],
                "reflection": scores["reflection"],
                "transformation": scores["transformation"],
            }
            store.append({"name": name, "class_code": st.session_state.class_code,
                          "scores": scores, "timestamp": datetime.now().strftime("%H:%M")})
            sheets_ok = submit_to_sheets(row)
            st.session_state.submitted = True
            st.session_state.sheets_ok = sheets_ok
            st.rerun()
    else:
        sheets_ok = st.session_state.get("sheets_ok", False)
        extra = "and saved to the research dataset ✓" if sheets_ok else "(Google Sheets not configured yet)"
        st.markdown(f"""
        <div class="confirm-box">
          <h3>✅ Submitted to Class Dashboard</h3>
          <p>Your profile is live in the facilitator view {extra}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    if st.button("🔄 Retake Diagnostic"):
        for k in ["page", "q_idx", "order", "answers", "submitted", "sheets_ok"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown("<p style='text-align:center;color:#CBD5E1;font-size:0.78rem;margin-top:1rem'>"
                "Inspired by Akkerman & Bakker (2011) boundary-crossing theory.</p>",
                unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    apply_css()
    init_state()
    facilitator_sidebar()
    if st.session_state.fac_mode:
        show_facilitator()
    elif st.session_state.page == "welcome":
        show_welcome()
    elif st.session_state.page == "quiz":
        show_quiz()
    elif st.session_state.page == "results":
        show_results()

if __name__ == "__main__":
    main()
