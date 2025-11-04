import os
import io
import random
import streamlit as st
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------
# App configuration
# ------------------------------------------------------------
st.set_page_config(page_title="The Boundary Compass", page_icon="🧭", layout="centered")

TITLE = "🧭 The Boundary Compass — Singapore Workplace Edition"
SUB = "A short reflective game on how you show up at boundaries: Identification · Coordination · Reflection · Transformation"

INTRO = """
In complex work, the toughest moments live **at the boundaries** — between roles, functions, values, and systems.

This game helps you notice your **preferred way of crossing boundaries**, based on four learning mechanisms:

- **Identification (I)** — seeing and naming differences & purpose clearly  
- **Coordination (C)** — building shared routines, tools, agreements  
- **Reflection (R)** — making sense across perspectives through dialogue  
- **Transformation (T)** — prototyping hybrid practices and embedding change

Choose what you would **most likely** do in each situation.  
At the end, you’ll see your **Boundary Compass** profile, an archetype, a **pictorial result card**, and stretch prompts.
"""

FOOTER = "*Mechanisms adapted from boundary-crossing research (Akkerman & Bakker, 2011).*"

IMAGES_DIR = "images"  # put your PNG/JPG here

# ------------------------------------------------------------
# 12 short, role-neutral Singapore workplace scenarios
# Add an 'img' key for a banner image per scenario (optional)
# ------------------------------------------------------------
SCENARIOS = [
    {
        "key": "s1",
        "title": "The Idea That Lands Flat",
        "context": "You share an idea in a meeting that you think could help. No one reacts. The silence is awkward.",
        "why": "You could withdraw, push harder, or try a different way to engage. How do you respond?",
        "img": f"{IMAGES_DIR}/s1.png",
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
        "img": f"{IMAGES_DIR}/s2.png",
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
        "img": f"{IMAGES_DIR}/s3.png",
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
        "img": f"{IMAGES_DIR}/s4.png",
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
        "img": f"{IMAGES_DIR}/s5.png",
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
        "img": f"{IMAGES_DIR}/s6.png",
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
        "img": f"{IMAGES_DIR}/s7.png",
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
        "img": f"{IMAGES_DIR}/s8.png",
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
        "img": f"{IMAGES_DIR}/s9.png",
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
        "img": f"{IMAGES_DIR}/s10.png",
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
        "img": f"{IMAGES_DIR}/s11.png",
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
        "img": f"{IMAGES_DIR}/s12.png",
        "opts": [
            ("Acknowledge what went well and who made it happen.", "I"),
            ("Create a five-minute retrospective at the next stand-up.", "C"),
            ("Ask what surprised or challenged people most.", "R"),
            ("Turn insights into a new team ritual for learning and gratitude.", "T"),
        ],
    },
]

# ------------------------------------------------------------
# Archetypes + tags/colours for pictorial card
# ------------------------------------------------------------
ARCHETYPE_META = {
    "IT": {"name": "🧩 Lego Synthesiser",
           "desc": "You integrate old and new wisely, re-assembling pieces into better forms.",
           "color": (50, 115, 220), "tags": ["Integrative", "Inventive", "Pragmatic"]},
    "IC": {"name": "🎫 EZ-Link Navigator",
           "desc": "You read systems quickly and help people move through rules and structures.",
           "color": (23, 165, 137), "tags": ["Organised", "Reliable", "Clear"]},
    "CR": {"name": "🧂 Condiment Connector",
           "desc": "You blend people and process; things go smoother when you’re around.",
           "color": (241, 196, 15), "tags": ["Inclusive", "Diplomatic", "Steady"]},
    "RT": {"name": "🥫 Milo Tin Transformer",
           "desc": "You learn fast and repurpose experience into creative new practice.",
           "color": (142, 68, 173), "tags": ["Creative", "Adaptive", "Bold"]},
    "IR": {"name": "🪞 Kopitiam Mirror",
           "desc": "You surface assumptions and help others see clearly — with care and calm.",
           "color": (84, 153, 199), "tags": ["Insightful", "Grounded", "Thoughtful"]},
    "CT": {"name": "🧰 Swiss Knife Collaborator",
           "desc": "You make innovation operational — bridging ideas into routines.",
           "color": (46, 134, 171), "tags": ["Versatile", "Hands-on", "Systemic"]},
    "ALL": {"name": "🌀 Boundary Alchemist",
            "desc": "You flex across all four mechanisms and catalyse learning in others.",
            "color": (88, 101, 242), "tags": ["Balanced", "Catalytic", "Versatile"]},
    "LOW": {"name": "🪑 The Settler",
            "desc": "You stabilise the space; with gentle stretch you’ll expand your range.",
            "color": (149, 165, 166), "tags": ["Grounding", "Dependable"]},
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

def safe_load_image(path: str, width: int = 900):
    try:
        if path and os.path.exists(path):
            img = Image.open(path).convert("RGB")
            w, h = img.size
            scale = width / float(w)
            new_h = int(h * scale)
            return img.resize((width, new_h), Image.LANCZOS)
    except Exception:
        pass
    return None

# ------------------------------------------------------------
# Result card generator (Pillow)
# ------------------------------------------------------------
def generate_result_card(archetype_code: str, scores: dict, width: int = 1080, height: int = 1440):
    meta = ARCHETYPE_META[archetype_code]
    bg = Image.new("RGB", (width, height), color=meta["color"])
    draw = ImageDraw.Draw(bg)

    # Try to load a nicer font if present; fallback to default
    try:
        # place a TTF font in repo (e.g., NotoSans) and point to it here if you wish
        font_big = ImageFont.truetype("NotoSans-Bold.ttf", 72)
        font_mid = ImageFont.truetype("NotoSans-Bold.ttf", 44)
        font_small = ImageFont.truetype("NotoSans-Regular.ttf", 36)
    except Exception:
        font_big = ImageFont.load_default()
        font_mid = ImageFont.load_default()
        font_small = ImageFont.load_default()

    pad = 60
    # white panel
    panel = Image.new("RGB", (width - pad*2, height - pad*2), color=(250, 250, 250))
    bg.paste(panel, (pad, pad))

    # Title
    title = f"You are… {meta['name']}"
    draw.text((pad+40, pad+30), title, fill=(30, 30, 30), font=font_big)

    # Description
    draw.text((pad+40, pad+140), meta["desc"], fill=(50, 50, 50), font=font_mid)

    # Tags
    y = pad + 260
    for tag in meta["tags"]:
        pill = f"  {tag}  "
        draw.text((pad+40, y), pill, fill=(255, 255, 255), font=font_small)
        y += 56

    # Scores box
    sx, sy = pad+40, y + 20
    draw.text((sx, sy), "Your Boundary Compass:", fill=(30, 30, 30), font=font_mid)
    sy += 60
    for label, key in [("I", "I"), ("C", "C"), ("R", "R"), ("T", "T")]:
        line = f"{label}: {scores[key]}"
        draw.text((sx, sy), line, fill=(60, 60, 60), font=font_small)
        sy += 44

    # Footer prompt
    draw.text((pad+40, height - pad - 180),
              "How will you use your strengths — and stretch one new mechanism — this week?",
              fill=(40, 40, 40), font=font_small)

    bio = io.BytesIO()
    bg.save(bio, format="PNG")
    bio.seek(0)
    return bio

# ------------------------------------------------------------
# UI
# ------------------------------------------------------------
def scenario_ui(index: int):
    sc = SCENARIOS[index]
    # Banner image
    banner = safe_load_image(sc.get("img"))
    if banner:
        st.image(banner, use_column_width=True)
    st.markdown(f"### {sc['title']}")
    st.caption(sc["context"])
    with st.expander("Why this matters", expanded=False):
        st.write(sc["why"])

    options = [label for (label, _m) in sc["opts"]]
    prev = st.session_state.answers.get(index, None)
    default = options.index(prev) if prev in options else 0  # mobile-friendly
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
    meta = ARCHETYPE_META[code]
    st.markdown(f"## {meta['name']}")
    st.write(meta["desc"])

    # Stretch guidance
    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dom = [ordered[0][0], ordered[1][0]]
    dom_text = " and ".join({"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}[d] for d in dom)
    st.markdown(f"**Your pattern:** You tend to begin boundary work through *{dom_text}*.")

    st.markdown("**Your next edge:**")
    for mech, _ in underused(scores):
        label = {"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}[mech]
        st.write(f"- *{label}*: {MICRO_PRACTICES[mech]}")

    st.divider()
    st.markdown("**One small reflection for the week:** Which upcoming situation might test your Compass — and what tiny experiment will you try?")

    # Generate and show the pictorial result card + download button
    card_png = generate_result_card(code, scores)
    st.image(card_png, caption="Tap and hold to save — or use the download button below.", use_column_width=True)
    st.download_button("⬇️ Download your result card (PNG)", data=card_png, file_name="boundary_compass_card.png", mime="image/png")

    st.caption(FOOTER)

# ------------------------------------------------------------
# App flow
# ------------------------------------------------------------
def main():
    if "order" not in st.session_state:
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

if __name__ == "__main__":
    main()