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
At the end, you’ll see your **Boundary Compass** profile, a pictorial result card, and concrete micro-practices to try next week.
"""

FOOTER = "*Mechanisms adapted from boundary-crossing research (Akkerman & Bakker, 2011).*"
IMAGES_DIR = "images"  # optional banner images live here (s1.png ... s12.png)

# ------------------------------------------------------------
# Scenarios (12): short, role-neutral, SG/ASEAN workplace
# Optional 'img' per scenario: images/sX.png (hide if missing)
# ------------------------------------------------------------
SCENARIOS = [
    {
        "key": "s1",
        "title": "The Idea That Lands Flat",
        "context": "You share an idea in a meeting. No one reacts. The silence is awkward.",
        "why": "You could withdraw, push harder, or try a different way to engage.",
        "img": f"{IMAGES_DIR}/s1.png",
        "opts": [
            ("Clarify the problem you were solving and restate your intent.", "I"),
            ("Ask for quick feedback or invite others to build on it together.", "C"),
            ("Pause and reflect: what might make others hesitant to respond?", "R"),
            ("Prototype your idea quietly and share results later.", "T"),
        ],
    },
    {
        "key": "s2",
        "title": "The Overloaded Team",
        "context": "Your team has been at full capacity; a new project lands unexpectedly.",
        "why": "People are tired, but the work matters.",
        "img": f"{IMAGES_DIR}/s2.png",
        "opts": [
            ("Clarify what’s truly essential and what can wait.", "I"),
            ("Re-prioritise tasks together and agree on timelines.", "C"),
            ("Ask how everyone is coping and what support they need.", "R"),
            ("Propose a new rhythm or workflow to make work sustainable.", "T"),
        ],
    },
    {
        "key": "s3",
        "title": "The Quiet Colleague",
        "context": "A capable teammate rarely speaks up, even when they have good ideas.",
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
        "context": "You’re added to a project halfway through. Goals and decisions are unclear, deadlines are close.",
        "why": "You could act fast, or slow down to orient yourself.",
        "img": f"{IMAGES_DIR}/s4.png",
        "opts": [
            ("Ask for clarity on purpose, roles, and current status.", "I"),
            ("Set up a short sync to align everyone quickly.", "C"),
            ("Observe for a bit to understand patterns and norms.", "R"),
            ("Sketch a one-page summary of what's known; test it with the group.", "T"),
        ],
    },
    {
        "key": "s5",
        "title": "The Tech Shortcut",
        "context": "A new AI tool could save hours of manual work, but no one has tested it yet.",
        "why": "There’s potential and risk.",
        "img": f"{IMAGES_DIR}/s5.png",
        "opts": [
            ("Define success criteria and constraints before adopting.", "I"),
            ("Run a one-week trial with check-in points.", "C"),
            ("Ask why people hesitate and what concerns they have.", "R"),
            ("Test on one process and share what you learn.", "T"),
        ],
    },
    {
        "key": "s6",
        "title": "The Feedback Moment",
        "context": "A peer asks, “Be honest — how was my presentation?” You saw strengths and gaps.",
        "why": "It’s a chance to help; tone matters.",
        "img": f"{IMAGES_DIR}/s6.png",
        "opts": [
            ("Ask what kind of feedback they want and how detailed.", "I"),
            ("Use a simple structure: 2 strengths, 2 improvements, 1 next step.", "C"),
            ("Reflect on why giving feedback feels tricky for you.", "R"),
            ("Offer to practise together before their next presentation.", "T"),
        ],
    },
    {
        "key": "s7",
        "title": "The Sticky Stakeholder",
        "context": "A senior stakeholder keeps changing direction. The team’s energy is fading.",
        "why": "You could comply, challenge, or help the system make sense.",
        "img": f"{IMAGES_DIR}/s7.png",
        "opts": [
            ("Clarify expectations and what success means this round.", "I"),
            ("Summarise changes and confirm decisions in writing.", "C"),
            ("Explore why priorities keep shifting — what’s upstream?", "R"),
            ("Co-create a shared decision tracker/playbook for future projects.", "T"),
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
        "context": "Two teammates disagree — one wants structure, the other experimentation.",
        "why": "Both have valid points. You’re in the middle.",
        "img": f"{IMAGES_DIR}/s9.png",
        "opts": [
            ("Clarify the problem we’re solving before choosing.", "I"),
            ("Agree on next steps: try one approach with review points.", "C"),
            ("Ask each to explain the principle behind their view.", "R"),
            ("Combine both ideas into a short pilot to test outcomes.", "T"),
        ],
    },
    {
        "key": "s10",
        "title": "The Change Rollout",
        "context": "A new policy launches and people groan: “Another change again?”",
        "why": "Change fatigue is real; the change matters too.",
        "img": f"{IMAGES_DIR}/s10.png",
        "opts": [
            ("Clarify what the change fixes and what stays the same.", "I"),
            ("Create a quick Q&A and feedback loop.", "C"),
            ("Ask what worries people most about new changes.", "R"),
            ("Turn early feedback into small tweaks that show responsiveness.", "T"),
        ],
    },
    {
        "key": "s11",
        "title": "The Sustainability Trade-Off",
        "context": "Your company wants to go greener, but sustainable materials slow production and raise costs.",
        "why": "Short-term targets clash with long-term commitments.",
        "img": f"{IMAGES_DIR}/s11.png",
        "opts": [
            ("Define what 'sustainability' means here; agree on boundaries.", "I"),
            ("Bring Finance, Ops, Sustainability together to review trade-offs.", "C"),
            ("Hold a dialogue on what 'responsible growth' means for the team.", "R"),
            ("Pilot a lower-impact process; measure cost and learning.", "T"),
        ],
    },
    {
        "key": "s12",
        "title": "The Small Win",
        "context": "The team just completed a tough sprint. Everyone rushes to the next task.",
        "why": "Celebration feels like a luxury; reflection builds capability.",
        "img": f"{IMAGES_DIR}/s12.png",
        "opts": [
            ("Acknowledge what went well and who made it happen.", "I"),
            ("Do a five-minute retro at the next stand-up.", "C"),
            ("Ask what surprised or challenged people most.", "R"),
            ("Turn insights into a new ritual for learning and gratitude.", "T"),
        ],
    },
]

# ------------------------------------------------------------
# Archetypes + tags/colours for result card
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
}

# Concrete, tangible micro-practices
MICRO_PRACTICES = {
    "I": "Run a 15-min 'kick-off clarity' chat before your next project. Capture purpose, roles, decision rights, and out-of-scope in a pinned doc.",
    "C": "Create ONE shared artefact this week (checklist, status template or dashboard) that two functions agree to use.",
    "R": "After a key meeting, host a 5-minute sense-making pause: 'What did we learn? What assumptions surfaced?' Capture 1 line per person.",
    "T": "Pick one cross-team pain point and run a 1-week mini-experiment (new handover, short sync, or co-lead trial). If useful, bake it into process.",
}

MECH_COLORS = {"I": (36, 113, 163), "C": (23, 165, 137), "R": (241, 196, 15), "T": (142, 68, 173)}

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
        if ans is None: continue
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
    mapping = {"IT":"IT","IC":"IC","CR":"CR","RT":"RT","IR":"IR","CT":"CT",
               "I":"IR","C":"CT","R":"RT","T":"IT"}
    return mapping.get(pair, mapping.get(primary, "ALL"))

def underused(scores):
    return sorted(scores.items(), key=lambda x: x[1])[:2]

def bar_chart(scores):
    cats = ["Identification (I)", "Coordination (C)", "Reflection (R)", "Transformation (T)"]
    vals = [scores["I"], scores["C"], scores["R"], scores["T"]]
    fig = go.Figure(go.Bar(
        x=vals, y=cats, orientation="h",
        marker=dict(color=[MECH_COLORS["I"], MECH_COLORS["C"], MECH_COLORS["R"], MECH_COLORS["T"]])
    ))
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10),
                      xaxis_title="Selections", yaxis_title="")
    return fig

# ---------- Imaging helpers ----------
def load_font(path, size):
    try: return ImageFont.truetype(path, size)
    except Exception: return ImageFont.load_default()

def draw_rounded_rect(draw, xy, radius, fill):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

def draw_pill(draw, x, y, text, font, pad=16, fill=(50,50,50), txt=(255,255,255)):
    w, h = draw.textbbox((0,0), text, font=font)[2:]
    draw.rounded_rectangle([x, y, x + w + pad*2, y + h + pad], radius=999, fill=fill)
    draw.text((x + pad, y + pad//2), text, font=font, fill=txt)

def draw_bar(draw, x, y, label, value, maxval, width, height, fill, font):
    draw.text((x, y), label, font=font, fill=(30,30,30))
    by = y + 30
    draw.rounded_rectangle([x, by, x + width, by + height], radius=height//2, fill=(230,230,230))
    if maxval > 0:
        vw = int(width * (value / maxval))
        draw.rounded_rectangle([x, by, x + vw, by + height], radius=height//2, fill=fill)

def safe_load_image(path: str, width: int = 960):
    try:
        if path and os.path.exists(path):
            img = Image.open(path).convert("RGB")
            w, h = img.size
            scale = width / float(w)
            return img.resize((width, int(h*scale)), Image.LANCZOS)
    except Exception:
        pass
    return None

# ---------- Pictorial result card ----------
def generate_result_card(archetype_code: str, scores: dict, width: int = 1080, height: int = 1440):
    meta = ARCHETYPE_META[archetype_code]
    img = Image.new("RGB", (width, height), color=meta["color"])
    draw = ImageDraw.Draw(img)

    pad = 60
    panel_xy = (pad, pad, width - pad, height - pad)
    draw_rounded_rect(draw, panel_xy, radius=48, fill=(250,250,250))

    title_f = load_font("NotoSans-Bold.ttf", 72)
    h1_f    = load_font("NotoSans-Bold.ttf", 44)
    body_f  = load_font("NotoSans-Regular.ttf", 34)
    tag_f   = load_font("NotoSans-Bold.ttf", 30)
    small_f = load_font("NotoSans-Regular.ttf", 28)

    x = pad + 40
    y = pad + 40
    draw.text((x, y), f"You are… {meta['name']}", font=title_f, fill=(30,30,30))
    y += 110
    draw.text((x, y), meta["desc"], font=h1_f, fill=(65,65,65))
    y += 100

    # Tag pills
    pill_x = x
    for tag in meta.get("tags", []):
        draw_pill(draw, pill_x, y, tag, tag_f, fill=(60,60,60))
        pill_x += draw.textbbox((0,0), tag, font=tag_f)[2] + 110
    y += 110

    draw.line([(x, y), (width - pad - 40, y)], fill=(220,220,220), width=3)
    y += 28
    draw.text((x, y), "Your Boundary Compass", font=h1_f, fill=(30,30,30))
    y += 60

    maxv = max(scores.values()) if max(scores.values()) > 0 else 1
    bar_w, bar_h, gap = (width - pad*2 - 120), 28, 22
    for label in ["I","C","R","T"]:
        draw_bar(draw, x, y, f"{label}: {scores[label]}", scores[label], maxv, bar_w, bar_h, MECH_COLORS[label], body_f)
        y += 30 + bar_h + gap

    footer_text = "How will you use your strengths — and stretch one new mechanism — this week?"
    draw.text((x, height - pad - 140), footer_text, font=small_f, fill=(50,50,50))

    bio = io.BytesIO()
    img.save(bio, format="PNG"); bio.seek(0)
    return bio

# ------------------------------------------------------------
# UI
# ------------------------------------------------------------
def scenario_ui(index: int):
    sc = SCENARIOS[index]
    banner = safe_load_image(sc.get("img"))
    if banner: st.image(banner, use_column_width=True)

    st.markdown(f"### {sc['title']}")
    st.caption(sc["context"])
    with st.expander("Why this matters", expanded=False):
        st.write(sc["why"])

    options = [label for (label, _m) in sc["opts"]]
    prev = st.session_state.answers.get(index, None)
    default = options.index(prev) if prev in options else 0
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

    ordered = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dom = [ordered[0][0], ordered[1][0]]
    dom_text = " and ".join({"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}[d] for d in dom)
    st.markdown(f"**Your pattern:** You tend to begin boundary work through *{dom_text}*.")

    st.markdown("**Your next edge (doable this week):**")
    for mech, _ in underused(scores):
        label = {"I":"Identification","C":"Coordination","R":"Reflection","T":"Transformation"}[mech]
        st.write(f"- **{label}** — {MICRO_PRACTICES[mech]}")

    st.divider()
    st.markdown("**One small reflection:** Which upcoming situation might test your Compass — and what tiny experiment will you try?")

    card_png = generate_result_card(code, scores)
    st.image(card_png, caption="Tap-and-hold to save (mobile) or use the button below.", use_column_width=True)
    st.download_button("⬇️ Download your result card (PNG)", data=card_png,
                       file_name="boundary_compass_card.png", mime="image/png")

    st.caption(FOOTER)

# ------------------------------------------------------------
# App flow
# ------------------------------------------------------------
def main():
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