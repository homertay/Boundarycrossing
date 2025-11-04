import os
import io
import random
import streamlit as st
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont

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

TITLE = "🧭 The Boundary Compass — Singapore Workplace Edition"
SUB = "A thoughtful, bite-sized game about how you respond at boundaries"

INTRO = """
Boundaries aren’t barriers — they’re where learning happens.

This game surfaces how you tend to cross boundaries using four mechanisms:
**Identification (I)** – clarifying purpose & differences  
**Coordination (C)** – building shared routines or tools  
**Reflection (R)** – making sense through dialogue  
**Transformation (T)** – turning insights into new practices

Choose what you would **most likely** do in each dilemma.
After each choice, take a beat for a **reflection nudge** — then move on.
"""

FOOTER = "*Based on boundary-crossing research by Akkerman & Bakker (2011).*"
IMAGES_DIR = "images"   # optional; app runs fine without images
FONTS = {"bold":"NotoSans-Bold.ttf", "regular":"NotoSans-Regular.ttf"}  # optional; app falls back if missing

# ============================================================
# RICH SCENARIOS (12) — role-neutral SG/ASEAN workplace
# ============================================================
SCENARIOS = [
    {
        "key": "s1",
        "title": "The Idea That Lands Flat",
        "context": (
            "Midway through a busy meeting, you share what you believe is a practical idea that could remove a recurring bottleneck. "
            "A few people look at their screens; someone changes topic. No one objects, but the idea seems to evaporate. "
            "You sense that timing, status, or framing may have affected how it landed."
        ),
        "why": (
            "This isn’t about right/wrong — it’s how you read the room and move the idea without forcing it. "
            "You can clarify purpose, build a bridge, seek meaning, or quietly prototype."
        ),
        "opts": [
            ("Restate the problem the idea solves and ask if the pain is still real.", "I"),
            ("Invite two colleagues to co-shape it into a 1-pager before the next session.", "C"),
            ("Ask a trusted peer later: what made the room go quiet — timing, ownership, or risk?", "R"),
            ("Run a 1-week micro-test on a small scope and bring evidence back.", "T"),
        ],
    },
    {
        "key": "s2",
        "title": "The Overloaded Team",
        "context": (
            "Your team has been sprinting for weeks. A strategic project now drops in with senior visibility and a tight runway. "
            "People care about the work, but energy and patience are thin. Quietly, trade-offs are already happening."
        ),
        "why": (
            "The question isn’t only ‘Can we do it?’ but ‘How do we do it without costing the team more than it can bear?’ "
            "You can set boundaries, create structure, host a human conversation, or redesign the way of working."
        ),
        "opts": [
            ("Clarify what outcome is non-negotiable and what can be de-scoped or delayed.", "I"),
            ("Co-prioritise tasks, freeze lower-value work, and publish a visible plan.", "C"),
            ("Surface the human reality in a short check-in: what support do we need to do this well?", "R"),
            ("Trial a new rhythm (focus blocks, no-meeting windows) for two weeks and review.", "T"),
        ],
    },
    {
        "key": "s3",
        "title": "The Quiet Colleague",
        "context": (
            "A colleague who thinks deeply rarely speaks in group settings. Their drafts are strong, but in meetings their ideas arrive late or not at all, and the team moves on. "
            "You sense both a personal preference and an environmental pattern."
        ),
        "why": (
            "This is a boundary of preference, safety, and group rhythm. "
            "You can name the gap, create a different container, explore the pattern, or design a practice that builds voice."
        ),
        "opts": [
            ("Check in privately: what conditions help them contribute live vs async?", "I"),
            ("Move early ideation to trios/async notes, then harvest in the meeting.", "C"),
            ("Reflect with the team on who gets airtime and when — to notice, not to blame.", "R"),
            ("Invite the colleague to co-lead a small segment next week with a clear brief.", "T"),
        ],
    },
    {
        "key": "s4",
        "title": "The Missing Context",
        "context": (
            "You join a programme mid-stream. Decisions have been made; documents exist but don’t align; the calendar is unforgiving. Different people give slightly different versions of the story."
        ),
        "why": (
            "Speed is tempting; so is analysis. The leadership move is sense-making that unlocks action. "
            "You can clarify anchors, coordinate alignment, reflect on patterns, or synthesise a map to test."
        ),
        "opts": [
            ("Ask for anchor clarity: purpose, scope, decision-rights, and current risks.", "I"),
            ("Book a 20-minute alignment huddle to name three truths and three unknowns.", "C"),
            ("Watch two ceremonies to read norms, language, and power dynamics.", "R"),
            ("Create a 1-page ‘Where we are/Where we’re heading’ map and iterate.", "T"),
        ],
    },
    {
        "key": "s5",
        "title": "The Tech Shortcut",
        "context": (
            "A new AI tool might cut manual effort by half. Excitement mixes with worry about quality, privacy, and the learning curve. "
            "No one wants to be the first to fail publicly."
        ),
        "why": (
            "Adoption is a boundary between risk and reward. You can define what ‘good’ is, scaffold a safe pilot, surface fears, or craft a new hybrid workflow."
        ),
        "opts": [
            ("Define success/guardrails (data, accuracy, review) before anyone tests it.", "I"),
            ("Run a bounded pilot with checkpoints and a simple decision tree.", "C"),
            ("Hold a short ‘hopes & worries’ round — note what trust would look like.", "R"),
            ("Redesign the task as ‘AI drafts, human curates’; publish the pattern if it works.", "T"),
        ],
    },
    {
        "key": "s6",
        "title": "The Feedback Moment",
        "context": (
            "A peer says, ‘Be honest — how was my presentation?’ You saw strong thinking but a muddy storyline and slides with too much text. They look nervous yet eager."
        ),
        "why": (
            "This is less about judgement and more about growth. You can clarify what feedback they want, structure the conversation, explore your own hesitation, or move into practice together."
        ),
        "opts": [
            ("Ask what kind of feedback is most useful now — big picture, delivery, or slide craft.", "I"),
            ("Use a structure: two strengths, two improvements, one next step.", "C"),
            ("Notice and name your own hesitation — fear of hurting or fear of conflict?", "R"),
            ("Offer a 30-min re-rehearsal and co-edit three slides together.", "T"),
        ],
    },
    {
        "key": "s7",
        "title": "The Sticky Stakeholder",
        "context": (
            "A senior stakeholder keeps pivoting the brief as new inputs arrive. The team’s patience is fraying; work gets redone; trust is thinning."
        ),
        "why": (
            "You could escalate, absorb, or enable better decision hygiene. The leadership move is to help the system decide better next time."
        ),
        "opts": [
            ("Clarify ‘done for this round’: decision scope, criteria, and success signal.", "I"),
            ("Summarise pivots and confirm in writing with a simple ‘version/decision’ log.", "C"),
            ("Ask upstream: what pressures/incentives are driving the zig-zag?", "R"),
            ("Co-design a lightweight playbook: roles, gates, and timeboxes.", "T"),
        ],
    },
    {
        "key": "s8",
        "title": "The Missed Deadline",
        "context": (
            "A dependency slipped and several teams were impacted. You were one of many moving parts. The chat is now full of heat — some helpful, some not."
        ),
        "why": (
            "Accountability can harden into blame or open into learning. You can name your part, coordinate recovery, reflect on the system, or change the way of working."
        ),
        "opts": [
            ("Own your slice: what you knew, decided, and will do differently.", "I"),
            ("Call a 20-min reset with affected teams; publish the new timeline.", "C"),
            ("Ask: which assumptions and signals did we miss across teams?", "R"),
            ("Propose a new handover pattern (checklist + single owner) and pilot it.", "T"),
        ],
    },
    {
        "key": "s9",
        "title": "The Team Debate",
        "context": (
            "Two colleagues argue passionately: one wants a tight plan, the other a looser exploration. Both have good reasons; the room is splitting into camps."
        ),
        "why": (
            "Binary fights hide shared goals. You can reframe the problem, set a structure to try, seek the principles underneath, or run a safe-to-fail probe."
        ),
        "opts": [
            ("Re-ask: what core problem are we solving and by when?", "I"),
            ("Choose one path for two weeks with review points; document the bet.", "C"),
            ("Invite each to explain their principle (risk, speed, learning) without rebuttal.", "R"),
            ("Blend into a short pilot: structured milestones with open exploration inside.", "T"),
        ],
    },
    {
        "key": "s10",
        "title": "The Change Rollout",
        "context": (
            "A new policy launches. People groan: ‘Another change…’ They’ve seen many starts without finishes; trust needs rebuilding."
        ),
        "why": (
            "This is a boundary between intention and experience. You can clarify meaning, create a bridge for questions, host sense-making, or show responsiveness through tweaks."
        ),
        "opts": [
            ("Explain what this change fixes, what stays the same, and the timeline.", "I"),
            ("Open a Q&A doc with 48-hour responses and a change log.", "C"),
            ("Ask: what do people fear losing, and what would reassure them?", "R"),
            ("Use early feedback to adjust one rule this week and show the loop working.", "T"),
        ],
    },
    {
        "key": "s11",
        "title": "The Sustainability Trade-off",
        "context": (
            "Greener materials and processes align with public commitments, but will raise cost and slow delivery for several months. "
            "Finance worries about margins; Operations worries about throughput; the Sustainability team worries about credibility."
        ),
        "why": (
            "This is a boundary between values and viability. You can define terms, coordinate decision rules, invite conscience, or create a new metric/practice."
        ),
        "opts": [
            ("Define what ‘sustainable enough for this decision’ means; set the boundary.", "I"),
            ("Co-create a decision playbook with thresholds and review cadence.", "C"),
            ("Host a conscience dialogue: what message do we send by choosing X vs Y?", "R"),
            ("Pilot a blended path (profit × carbon intensity) and track publicly.", "T"),
        ],
    },
    {
        "key": "s12",
        "title": "The Small Win",
        "context": (
            "After weeks of effort, the team clears a tough milestone. Slack is quiet for two minutes and then everyone rushes to the next task."
        ),
        "why": (
            "Celebration and reflection are not indulgences; they build capability. You can name the win, add a simple ritual, harvest meaning, or embed the habit."
        ),
        "opts": [
            ("Name the win and who made it possible — in writing.", "I"),
            ("Add a 5-minute retro at the next stand-up (what worked/blocked/changed).", "C"),
            ("Ask each person for one surprise and one learning; capture in one slide.", "R"),
            ("Create a recurring ‘small wins’ ritual and rotate the host monthly.", "T"),
        ],
    },
]

# ============================================================
# REFLECTION NUDGES (shown after each choice)
# ============================================================
NUDGES = {
    "I": "You chose to begin with **Identification** — clarity can reduce noise. Watch for over-reliance on ‘stating’ without **testing**.",
    "C": "You leaned on **Coordination** — helpful when things scatter. Notice when process becomes protection from **trying**.",
    "R": "You went with **Reflection** — sense-making opens learning. Beware staying in analysis instead of **acting**.",
    "T": "You moved to **Transformation** — experiments shift systems. Check that new patterns still honour core **boundaries**."
}

# ============================================================
# ARCHETYPES + MICRO-PRACTICES
# ============================================================
ARCHETYPE_META = {
    "IT": {"name":"🧩 Lego Synthesiser","desc":"You integrate old and new wisely — re-assembling pieces into better forms.",
            "color":(50,115,220),"tags":["Integrative","Inventive","Pragmatic"]},
    "IC": {"name":"🎫 EZ-Link Navigator","desc":"You read systems quickly and help people move through rules and structures.",
            "color":(23,165,137),"tags":["Organised","Reliable","Clear"]},
    "CR": {"name":"🧂 Condiment Connector","desc":"You blend people and process; things go smoother when you’re around.",
            "color":(241,196,15),"tags":["Inclusive","Diplomatic","Steady"]},
    "RT": {"name":"🥫 Milo Tin Transformer","desc":"You learn fast and repurpose experience into creative new practice.",
            "color":(142,68,173),"tags":["Creative","Adaptive","Bold"]},
    "IR": {"name":"🪞 Kopitiam Mirror","desc":"You surface assumptions and help others see clearly — with care and calm.",
            "color":(84,153,199),"tags":["Insightful","Grounded","Thoughtful"]},
    "CT": {"name":"🧰 Swiss Knife Collaborator","desc":"You make innovation operational — bridging ideas into routines.",
            "color":(46,134,171),"tags":["Versatile","Hands-on","Systemic"]},
    "ALL":{"name":"🌀 Boundary Alchemist","desc":"You flex across all four mechanisms and catalyse learning in others.",
            "color":(88,101,242),"tags":["Balanced","Catalytic","Versatile"]},
}

MICRO_PRACTICES = {
    "I": "Run a 15-min **kick-off clarity** chat before your next project. Pin a 1-page note: purpose, roles, decision rights, out-of-scope.",
    "C": "Create **one shared artefact** this week (checklist, template, or dashboard) that two functions agree to use.",
    "R": "After a key meeting, host a 5-min **sense-making pause**: ‘What did we learn? What assumptions surfaced?’ Capture 1 line each.",
    "T": "Pick one cross-team pain point and run a **1-week mini-experiment** (new handover, short sync, or co-lead trial). If it works, bake it in."
}

MECH_COLORS = {"I":(36,113,163),"C":(23,165,137),"R":(241,196,15),"T":(142,68,173)}

# ============================================================
# STATE & SCORING
# ============================================================
def init_state():
    if "order" not in st.session_state:
        st.session_state.order = list(range(len(SCENARIOS)))
        random.shuffle(st.session_state.order)
    if "page" not in st.session_state: st.session_state.page = 0            # which scenario index (0..11)
    if "answers" not in st.session_state: st.session_state.answers = {i: None for i in range(len(SCENARIOS))}
    if "subpage" not in st.session_state: st.session_state.subpage = 0      # 0=question, 1=reflection

def score_mechanisms():
    s = {"I":0,"C":0,"R":0,"T":0}
    for i,a in st.session_state.answers.items():
        if a:
            for (opt,m) in SCENARIOS[i]["opts"]:
                if a == opt: s[m] += 1
    return s

def pick_archetype(scores):
    vals = list(scores.values()); spread = max(vals) - min(vals)
    if spread <= 1: return "ALL"
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary, secondary = ordered[0][0], ordered[1][0]
    pair = primary + secondary
    mapping = {"IT":"IT","IC":"IC","CR":"CR","RT":"RT","IR":"IR","CT":"CT",
               "I":"IR","C":"CT","R":"RT","T":"IT"}
    return mapping.get(pair, mapping.get(primary, "ALL"))

def underused(scores):
    return sorted(scores.items(), key=lambda x: x[1])[:2]

# ============================================================
# GRAPHICS HELPERS + RESULT CARD
# ============================================================
def load_font(path, size):
    try: return ImageFont.truetype(path, size)
    except Exception: return ImageFont.load_default()

def draw_bar(draw, x, y, label, val, maxv, w, h, fill, font):
    draw.text((x, y), label, font=font, fill=(30,30,30))
    by = y + 30
    draw.rounded_rectangle([x, by, x + w, by + h], radius=h//2, fill=(230,230,230))
    vw = int(w * (val/maxv)) if maxv > 0 else 0
    draw.rounded_rectangle([x, by, x + vw, by + h], radius=h//2, fill=fill)

def draw_pill(draw, x, y, text, font, pad=16, fill=(50,50,50), txt=(255,255,255)):
    w, h = draw.textbbox((0,0), text, font=font)[2:]
    draw.rounded_rectangle([x, y, x + w + pad*2, y + h + pad], radius=999, fill=fill)
    draw.text((x + pad, y + pad//2), text, font=font, fill=txt)

def generate_result_card(code, scores, width=1080, height=1920):
    meta = ARCHETYPE_META[code]; theme = meta["color"]
    img = Image.new("RGB",(width,height),theme); d = ImageDraw.Draw(img)
    # gradient
    for i in range(height):
        t = i/height
        r = int(theme[0]*(1-0.10*t) + 255*(0.10*t))
        g = int(theme[1]*(1-0.10*t) + 255*(0.10*t))
        b = int(theme[2]*(1-0.10*t) + 255*(0.10*t))
        d.line([(0,i),(width,i)], fill=(r,g,b))
    # panel
    pad = 60
    d.rounded_rectangle([pad,pad,width-pad,height-pad], radius=56, fill=(250,250,250))
    # fonts
    title_f = load_font(FONTS["bold"], 78)
    h1_f    = load_font(FONTS["bold"], 46)
    body_f  = load_font(FONTS["regular"], 36)
    tag_f   = load_font(FONTS["bold"], 32)
    small_f = load_font(FONTS["regular"], 30)
    # content
    x = pad + 52; y = pad + 80
    d.text((x,y), f"You are… {meta['name']}", font=title_f, fill=(30,30,30))
    y += 120; d.text((x,y), meta["desc"], font=h1_f, fill=(65,65,65))
    y += 120
    pill_x = x
    for tag in meta.get("tags", [])[:3]:
        draw_pill(d, pill_x, y, tag, tag_f, fill=(60,60,60)); pill_x += 260
    y += 110
    d.line([(x,y),(width-pad-52,y)], fill=(220,220,220), width=4); y += 40
    d.text((x,y), "Your Boundary Compass", font=h1_f, fill=(30,30,30)); y += 64
    maxv = max(scores.values()) if max(scores.values())>0 else 1
    bw, bh, gap = (width-pad*2-120), 36, 28
    for k in ["I","C","R","T"]:
        draw_bar(d, x, y, f"{k}: {scores[k]}", scores[k], maxv, bw, bh, MECH_COLORS[k], body_f)
        y += 40 + bh + gap
    d.text((x, height-pad-180),
           "Use your strengths — and stretch one new mechanism — this week.",
           font=small_f, fill=(60,60,60))
    bio = io.BytesIO(); img.save(bio, "PNG", optimize=True); bio.seek(0); return bio

# ============================================================
# UI — SCENARIO + REFLECTION NUDGE + RESULTS
# ============================================================
def scenario_ui(i):
    sc = SCENARIOS[i]
    if st.session_state.subpage == 0:
        # QUESTION PAGE
        st.markdown(f"### {sc['title']}")
        st.caption(sc["context"])
        with st.expander("Why this matters", expanded=False):
            st.write(sc["why"])
        options = [o for (o,_m) in sc["opts"]]
        prev = st.session_state.answers.get(i)
        default = options.index(prev) if prev in options else 0
        choice = st.radio("What would you most likely do?",
                          options, index=default, label_visibility="collapsed", key=f"q_{i}")
        c1, c2 = st.columns(2)
        if c1.button("◀ Back", disabled=(st.session_state.page == 0), use_container_width=True):
            st.session_state.page -= 1
            st.session_state.subpage = 0
            st.rerun()
        if c2.button("Next ▶", use_container_width=True):
            st.session_state.answers[i] = choice
            st.session_state.subpage = 1   # go to reflection nudge
            st.rerun()
    else:
        # REFLECTION NUDGE PAGE
        # find mechanism of chosen option
        picked = st.session_state.answers[i]
        mech = None
        for (opt,m) in SCENARIOS[i]["opts"]:
            if opt == picked: mech = m; break
        st.info(f"**You chose:** {picked}")
        st.markdown(f"### Quick reflection")
        st.write(NUDGES.get(mech, "Notice what this move opens — and what it might miss."))
        st.markdown("> One question before you continue: *What small risk would you take next to balance this move?*")
        c = st.button("Continue ▶", use_container_width=True)
        if c:
            st.session_state.subpage = 0
            st.session_state.page += 1
            st.rerun()

def results_ui():
    scores = score_mechanisms()
    st.success("🎉 You’ve completed your Boundary Compass journey.")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("I", scores["I"]); c2.metric("C", scores["C"]); c3.metric("R", scores["R"]); c4.metric("T", scores["T"])
    fig = go.Figure(go.Bar(
        x=[scores["I"], scores["C"], scores["R"], scores["T"]],
        y=["I","C","R","T"], orientation="h",
        marker=dict(color=[MECH_COLORS[k] for k in ["I","C","R","T"]])
    ))
    fig.update_layout(height=320, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

    code = pick_archetype(scores); meta = ARCHETYPE_META[code]
    st.markdown(f"## {meta['name']}"); st.write(meta["desc"])

    st.markdown("**Your next edge (simple and doable this week):**")
    for mech,_ in underused(scores):
        st.write(f"- **{mech}** — {MICRO_PRACTICES[mech]}")

    st.divider()
    st.write("**One small reflection:** Which upcoming situation might test your Compass — and what tiny experiment will you try?**")

    # Result card + download
    card = generate_result_card(code, scores)
    st.image(card, use_column_width=True, caption="Save or screenshot your result card.")
    st.download_button("⬇️ Download result card", data=card, file_name="BoundaryCompass.png", mime="image/png")

    st.caption(FOOTER)

# ============================================================
# APP FLOW
# ============================================================
def main():
    apply_css()
    init_state()

    st.title(TITLE)
    st.caption(SUB)
    with st.expander("What is this about?", expanded=False):
        st.markdown(INTRO)

    st.progress((st.session_state.page + st.session_state.subpage*0.5) / len(SCENARIOS))

    if st.session_state.page < len(SCENARIOS):
        idx = st.session_state.order[st.session_state.page]
        scenario_ui(idx)
    else:
        results_ui()

if __name__ == "__main__":
    main()