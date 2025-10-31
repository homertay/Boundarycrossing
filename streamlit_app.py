import json
import streamlit as st
import plotly.graph_objects as go

# -------------------------
# 20 items grounded in boundary-crossing theory
# -------------------------
QUESTIONS = [
    # Identification
    {"id": 1, "mechanism": "Identification", "text": "I can name the key differences in goals and language between my team and a partner team."},
    {"id": 2, "mechanism": "Identification", "text": "Before collaborating, I map stakeholders’ incentives, constraints, and decision rights."},
    {"id": 3, "mechanism": "Identification", "text": "I notice when two groups use different terms for the same idea and call it out to align meaning."},
    {"id": 4, "mechanism": "Identification", "text": "I can articulate my team’s norms and blind spots without becoming defensive."},
    {"id": 5, "mechanism": "Identification", "text": "I deliberately observe how boundaries (departmental, cultural, or professional) shape decision-making in my organisation."},

    # Coordination
    {"id": 6, "mechanism": "Coordination", "text": "I introduce shared artefacts (logic models, dashboards, templates) to coordinate work across groups."},
    {"id": 7, "mechanism": "Coordination", "text": "I simplify jargon and translate between technical and non-technical colleagues in real time."},
    {"id": 8, "mechanism": "Coordination", "text": "I design lightweight routines that help information move smoothly between teams."},
    {"id": 9, "mechanism": "Coordination", "text": "When priorities clash, I negotiate minimal viable agreements so work can continue."},
    {"id": 10, "mechanism": "Coordination", "text": "I help different groups use a common framework or language to describe their outcomes."},

    # Reflection
    {"id": 11, "mechanism": "Reflection", "text": "Working with people from other disciplines often changes how I think about my own work."},
    {"id": 12, "mechanism": "Reflection", "text": "I seek feedback from colleagues who see a challenge from a completely different angle."},
    {"id": 13, "mechanism": "Reflection", "text": "I pause projects occasionally to ask, 'What assumptions are we making here?'"},    
    {"id": 14, "mechanism": "Reflection", "text": "I share stories of what I’ve learned from mistakes or mismatched expectations."},
    {"id": 15, "mechanism": "Reflection", "text": "I use reflective spaces (retrospectives, journaling, dialogue) to make learning visible."},

    # Transformation
    {"id": 16, "mechanism": "Transformation", "text": "I co-create new ways of working that combine multiple frameworks or disciplines."},
    {"id": 17, "mechanism": "Transformation", "text": "I test boundary-spanning solutions with diverse users before scaling."},
    {"id": 18, "mechanism": "Transformation", "text": "I tell integrative stories that help different stakeholders see a shared vision."},
    {"id": 19, "mechanism": "Transformation", "text": "I willingly retire legacy practices when a better co-created alternative appears."},
    {"id": 20, "mechanism": "Transformation", "text": "I mentor others to design across boundaries and sustain collaborative practices."},
]

# Archetype mapping
ARCHETYPES = {
    "Boundary Mapper": {"mechanisms": ["Identification"], "emoji": "🗺",
        "summary": "Sees and names boundaries clearly; surfaces invisible assumptions.",
        "tip": "Move from describing boundaries to designing crossings."},
    "Bridge Architect": {"mechanisms": ["Coordination"], "emoji": "🔗",
        "summary": "Builds routines and artefacts that connect diverse people and systems.",
        "tip": "Balance process with purpose—connect hearts as well as systems."},
    "Reflective Sense-Maker": {"mechanisms": ["Reflection"], "emoji": "🪞",
        "summary": "Turns difference into learning; models curiosity and psychological safety.",
        "tip": "Translate reflection into one visible change."},
    "Ecosystem Catalyst": {"mechanisms": ["Transformation"], "emoji": "🌾",
        "summary": "Co-creates new practices and stories that unite perspectives.",
        "tip": "Codify innovations so others can adopt them."},
    "System Navigator": {"mechanisms": ["Identification", "Coordination"], "emoji": "🧭",
        "summary": "Connects strategy, people, and data; aligns agendas across levels.",
        "tip": "Slow down for reflection—make learning visible."},
    "Integrative Weaver": {"mechanisms": ["Identification","Coordination","Reflection","Transformation"], "emoji": "🕸",
        "summary": "Balances mapping, bridging, reflecting, and transforming; mentors others to weave.",
        "tip": "Build institutional pathways so weaving continues beyond you."}
}

# --- Streamlit App ---
st.set_page_config(page_title="Boundary-Crossing Leadership Survey", page_icon="🧭", layout="centered")
st.title("🧭 Boundary-Crossing Leadership Survey")
st.write("""
20 statements measure how you lead across boundaries—grounded in Akkerman & Bakker’s
mechanisms: **Identification, Coordination, Reflection, Transformation**.
""")

with st.expander("What these mechanisms mean"):
    st.markdown("""
- **Identification** – seeing differences clearly and naming boundaries  
- **Coordination** – building bridges through shared tools and routines  
- **Reflection** – learning by seeing through others’ perspectives  
- **Transformation** – co-creating new practices that integrate worlds
""")

st.divider()
responses = {}
for q in QUESTIONS:
    responses[q["id"]] = st.slider(f"{q['id']}. {q['text']}", 1, 5, 3)

if st.button("Calculate My Profile"):
    # Aggregate
    sums, counts = {}, {}
    for q in QUESTIONS:
        m = q["mechanism"]
        sums[m] = sums.get(m,0) + responses[q["id"]]
        counts[m] = counts.get(m,0) + 1
    avg = {m: round(sums[m]/counts[m],2) for m in sums}

    st.subheader("Your Mechanism Scores")
    st.write(avg)

    # Radar
    cats = list(avg.keys())
    vals = list(avg.values())
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=vals+[vals[0]], theta=cats+[cats[0]], fill='toself'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1,5])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Determine archetype
    spread = max(avg.values()) - min(avg.values())
    if spread <= 0.4:
        archetype = "Integrative Weaver"
    elif abs(avg["Identification"] - avg["Coordination"]) <= 0.2 and \
         avg["Identification"] > avg["Reflection"]+0.3 and avg["Identification"] > avg["Transformation"]+0.3:
        archetype = "System Navigator"
    else:
        top = max(avg, key=avg.get)
        mapping = {
            "Identification": "Boundary Mapper",
            "Coordination": "Bridge Architect",
            "Reflection": "Reflective Sense-Maker",
            "Transformation": "Ecosystem Catalyst"
        }
        archetype = mapping[top]

    info = ARCHETYPES[archetype]
    st.markdown(f"## Your Archetype: {info['emoji']} **{archetype}**")
    st.write(info["summary"])
    st.markdown(f"**Growth tip:** {info['tip']}")

    st.download_button(
        "Download My Results (JSON)",
        data=json.dumps({"scores": avg, "archetype": archetype}, indent=2),
        file_name="boundary_profile.json",
        mime="application/json"
    )

st.divider()
st.markdown("""
**Theory Anchors**
- Akkerman & Bakker (2011) Boundary Crossing & Boundary Objects  
- Star & Griesemer (1989) Boundary Objects  
- Carlile (2004) Knowledge Boundaries  
- Wenger (1998) Communities of Practice (brokering)
""")