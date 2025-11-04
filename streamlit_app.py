import os, io, random
import streamlit as st
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="The Boundary Compass", page_icon="🧭", layout="centered")

def apply_css():
    st.markdown("""
    <style>
      .stApp {background: linear-gradient(180deg,#F7FBFF 0%,#FFFFFF 60%);}
      .block-container {padding-top:2rem;padding-bottom:4rem;max-width:900px;}
      details {border-radius:12px;background:#fff;border:1px solid #ebeff3;}
      .stRadio > div {gap:.75rem;}
      .stRadio label {
        background:#fff;border:1px solid #e5ecf3;border-radius:12px;
        padding:.9rem 1rem;width:100%;transition:all .12s ease;
      }
      .stRadio label:hover {border-color:#c3d5ea;background:#f9fcff;}
      #MainMenu, header, footer {visibility:hidden;}
    </style>
    """, unsafe_allow_html=True)

TITLE = "🧭 The Boundary Compass — Singapore Workplace Edition"
SUB = "Reflective quiz: How do you show up at boundaries?"
INTRO = """
Boundaries aren’t barriers—they’re where learning happens.

This game shows how you tend to cross boundaries using four mechanisms:
**Identification (I)** – clarifying purpose & differences  
**Coordination (C)** – building routines or shared tools  
**Reflection (R)** – making sense through dialogue  
**Transformation (T)** – turning insights into new practices
"""

FOOTER = "*Based on boundary-crossing research by Akkerman & Bakker (2011).*"
IMAGES_DIR = "images"

# ------------------------------------------------------------
# SCENARIOS (12 concise, role-neutral Singapore workplace cases)
# ------------------------------------------------------------
SCENARIOS = [
    {"key":"s1","title":"The Idea That Lands Flat",
     "context":"You share an idea; the room is silent.",
     "why":"You could withdraw, push harder, or try a new angle.",
     "opts":[
       ("Restate the problem you were solving; check alignment.","I"),
       ("Invite feedback; co-build it on the spot.","C"),
       ("Notice who looked uncertain—ask later why.","R"),
       ("Prototype it quietly; show evidence next round.","T"),
     ]},
    {"key":"s2","title":"The Overloaded Team",
     "context":"A new project lands; your team’s already maxed out.",
     "why":"People are tired, but the work matters.",
     "opts":[
       ("Clarify what’s essential and what can wait.","I"),
       ("Re-prioritise tasks and set joint timelines.","C"),
       ("Ask how everyone’s coping and what support helps.","R"),
       ("Suggest a new rhythm to make workload sustainable.","T"),
     ]},
    {"key":"s3","title":"The Quiet Colleague",
     "context":"A capable teammate rarely speaks up.",
     "why":"You sense a missed chance for learning.",
     "opts":[
       ("Check privately on their comfort level.","I"),
       ("Create smaller discussions where all contribute.","C"),
       ("Reflect on why some voices go unheard.","R"),
       ("Co-lead a task to help them gain confidence.","T"),
     ]},
    {"key":"s4","title":"The Missing Context",
     "context":"You join a project mid-stream; deadlines loom.",
     "why":"Do you act fast or slow down to orient?",
     "opts":[
       ("Ask for purpose, roles, and progress so far.","I"),
       ("Run a quick sync to align everyone.","C"),
       ("Observe quietly to read patterns.","R"),
       ("Summarise what’s known; test it with the group.","T"),
     ]},
    {"key":"s5","title":"The Tech Shortcut",
     "context":"An AI tool could save hours, but no one’s tried it.",
     "why":"Potential meets uncertainty.",
     "opts":[
       ("Define success criteria and guardrails first.","I"),
       ("Run a short pilot with checkpoints.","C"),
       ("Ask what worries others about trying it.","R"),
       ("Test it on one task and share results.","T"),
     ]},
    {"key":"s6","title":"The Feedback Moment",
     "context":"A peer asks, 'Be honest—how was my presentation?'",
     "why":"You saw both strengths and gaps.",
     "opts":[
       ("Ask what feedback they want and how direct.","I"),
       ("Use a 2-plus-2-plus-1 method: two wins, two tips, one next step.","C"),
       ("Reflect on why feedback feels tricky for you.","R"),
       ("Offer to rehearse together before next time.","T"),
     ]},
    {"key":"s7","title":"The Sticky Stakeholder",
     "context":"A senior keeps changing direction; morale drops.",
     "why":"Comply, challenge, or help them clarify?",
     "opts":[
       ("Clarify success criteria for this round.","I"),
       ("Document decisions and confirm in writing.","C"),
       ("Explore upstream pressures behind the shifts.","R"),
       ("Co-design a decision tracker for future use.","T"),
     ]},
    {"key":"s8","title":"The Missed Deadline",
     "context":"A deliverable slips; others are affected.",
     "why":"Shared accountability moment.",
     "opts":[
       ("Acknowledge the miss and your role.","I"),
       ("Meet affected teams to reset timelines.","C"),
       ("Ask what blind spots contributed.","R"),
       ("Capture lessons; adjust workflow for next time.","T"),
     ]},
    {"key":"s9","title":"The Team Debate",
     "context":"Two teammates clash—structure vs. flexibility.",
     "why":"Both make sense; you’re in the middle.",
     "opts":[
       ("Clarify what problem you’re solving.","I"),
       ("Agree on one approach; review next week.","C"),
       ("Let each explain the principle behind their view.","R"),
       ("Blend both into a short pilot.","T"),
     ]},
    {"key":"s10","title":"The Change Rollout",
     "context":"A new policy triggers sighs: 'Another change?'",
     "why":"Fatigue meets necessity.",
     "opts":[
       ("Clarify what changes and what stays.","I"),
       ("Set up Q&A and feedback loop.","C"),
       ("Ask what people fear losing.","R"),
       ("Adapt based on early feedback.","T"),
     ]},
    {"key":"s11","title":"The Sustainability Trade-Off",
     "context":"Greener materials raise cost and slow production.",
     "why":"Short-term vs. long-term goals.",
     "opts":[
       ("Define what 'sustainability' means here.","I"),
       ("Bring Finance, Ops, Sustainability to weigh options.","C"),
       ("Discuss what 'responsible growth' means for us.","R"),
       ("Pilot a low-impact method; measure cost + learning.","T"),
     ]},
    {"key":"s12","title":"The Small Win",
     "context":"After a tough sprint, everyone rushes on.",
     "why":"Reflection often gets skipped.",
     "opts":[
       ("Acknowledge what went well and who made it happen.","I"),
       ("Add a 5-min retrospective to next stand-up.","C"),
       ("Ask what surprised or challenged people most.","R"),
       ("Turn insights into a recurring learning ritual.","T"),
     ]},
]

# ------------------------------------------------------------
# META
# ------------------------------------------------------------
ARCHETYPE_META = {
 "IT":{"name":"🧩 Lego Synthesiser","desc":"You integrate old and new wisely—re-assembling pieces into better forms.",
        "color":(50,115,220),"tags":["Integrative","Inventive","Pragmatic"]},
 "IC":{"name":"🎫 EZ-Link Navigator","desc":"You read systems quickly and help people move through rules and structures.",
        "color":(23,165,137),"tags":["Organised","Reliable","Clear"]},
 "CR":{"name":"🧂 Condiment Connector","desc":"You blend people and process; things go smoother when you’re around.",
        "color":(241,196,15),"tags":["Inclusive","Diplomatic","Steady"]},
 "RT":{"name":"🥫 Milo Tin Transformer","desc":"You learn fast and repurpose experience into creative new practice.",
        "color":(142,68,173),"tags":["Creative","Adaptive","Bold"]},
 "IR":{"name":"🪞 Kopitiam Mirror","desc":"You surface assumptions and help others see clearly—with care and calm.",
        "color":(84,153,199),"tags":["Insightful","Grounded","Thoughtful"]},
 "CT":{"name":"🧰 Swiss Knife Collaborator","desc":"You make innovation operational—bridging ideas into routines.",
        "color":(46,134,171),"tags":["Versatile","Hands-on","Systemic"]},
 "ALL":{"name":"🌀 Boundary Alchemist","desc":"You flex across all four mechanisms and catalyse learning in others.",
        "color":(88,101,242),"tags":["Balanced","Catalytic","Versatile"]},
}

MICRO_PRACTICES = {
 "I":"💡 Run a 15-min 'kick-off clarity' chat before your next project. Capture purpose, roles, and limits in a shared doc.",
 "C":"🧱 Create one shared artefact this week (checklist, dashboard, or ritual) that connects two functions.",
 "R":"🔍 After a key meeting, host a 5-min sense-making pause: 'What did we learn? What assumptions surfaced?'",
 "T":"🚀 Pick one cross-team pain point and run a 1-week experiment (new handover, short sync, or co-lead trial). If it works, bake it into process.",
}
MECH_COLORS = {"I":(36,113,163),"C":(23,165,137),"R":(241,196,15),"T":(142,68,173)}

# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------
def init_state():
    if "order" not in st.session_state:
        st.session_state.order = list(range(len(SCENARIOS))); random.shuffle(st.session_state.order)
    if "page" not in st.session_state: st.session_state.page = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {i:None for i in range(len(SCENARIOS))}

def score_mechanisms():
    s={"I":0,"C":0,"R":0,"T":0}
    for i,a in st.session_state.answers.items():
        if a:
            for (opt,m) in SCENARIOS[i]["opts"]:
                if a==opt: s[m]+=1
    return s

def pick_archetype(scores):
    vals=list(scores.values()); spread=max(vals)-min(vals)
    if spread<=1: return "ALL"
    ordered=sorted(scores.items(),key=lambda x:x[1],reverse=True)
    primary,secondary=ordered[0][0],ordered[1][0]
    pair=primary+secondary
    mapping={"IT":"IT","IC":"IC","CR":"CR","RT":"RT","IR":"IR","CT":"CT",
             "I":"IR","C":"CT","R":"RT","T":"IT"}
    return mapping.get(pair,mapping.get(primary,"ALL"))

def underused(scores): return sorted(scores.items(),key=lambda x:x[1])[:2]

# ------------------------------------------------------------
# GRAPHICS UTILITIES
# ------------------------------------------------------------
def load_font(path,size):
    try: return ImageFont.truetype(path,size)
    except Exception: return ImageFont.load_default()

def draw_bar(draw,x,y,label,val,maxv,w,h,fill,font):
    draw.text((x,y),label,font=font,fill=(30,30,30))
    by=y+30; draw.rounded_rectangle([x,by,x+w,by+h],radius=h//2,fill=(230,230,230))
    vw=int(w*(val/maxv)) if maxv>0 else 0
    draw.rounded_rectangle([x,by,x+vw,by+h],radius=h//2,fill=fill)

def draw_pill(draw,x,y,text,font,pad=16,fill=(50,50,50),txt=(255,255,255)):
    w,h=draw.textbbox((0,0),text,font=font)[2:]
    draw.rounded_rectangle([x,y,x+w+pad*2,y+h+pad],radius=999,fill=fill)
    draw.text((x+pad,y+pad//2),text,font=font,fill=txt)

# ------------------------------------------------------------
# RESULT CARD (high-res, screenshot-ready)
# ------------------------------------------------------------
def generate_result_card(code,scores,width=1080,height=1920):
    meta=ARCHETYPE_META[code]; theme=meta["color"]
    img=Image.new("RGB",(width,height),theme); d=ImageDraw.Draw(img)
    # subtle gradient
    for i in range(height):
        t=i/height
        r=int(theme[0]*(1-0.1*t)+255*(0.1*t))
        g=int(theme[1]*(1-0.1*t)+255*(0.1*t))
        b=int(theme[2]*(1-0.1*t)+255*(0.1*t))
        d.line([(0,i),(width,i)],fill=(r,g,b))
    # white panel
    pad=60; d.rounded_rectangle([pad,pad,width-pad,height-pad],radius=56,fill=(250,250,250))
    title_f=load_font("NotoSans-Bold.ttf",78)
    h1_f=load_font("NotoSans-Bold.ttf",46)
    body_f=load_font("NotoSans-Regular.ttf",36)
    tag_f=load_font("NotoSans-Bold.ttf",32)
    small_f=load_font("NotoSans-Regular.ttf",30)
    x=pad+52; y=pad+80
    d.text((x,y),f"You are… {meta['name']}",font=title_f,fill=(30,30,30))
    y+=120; d.text((x,y),meta["desc"],font=h1_f,fill=(65,65,65))
    y+=120
    pill_x=x
    for tag in meta.get("tags",[])[:3]:
        draw_pill(d,pill_x,y,tag,tag_f,fill=(60,60,60)); pill_x+=260
    y+=110; d.line([(x,y),(width-pad-52,y)],fill=(220,220,220),width=4); y+=40
    d.text((x,y),"Your Boundary Compass",font=h1_f,fill=(30,30,30)); y+=64
    maxv=max(scores.values()) if max(scores.values())>0 else 1
    bw,bh,gap=(width-pad*2-120),36,28
    for k in ["I","C","R","T"]:
        draw_bar(d,x,y,f"{k}: {scores[k]}",scores[k],maxv,bw,bh,MECH_COLORS[k],body_f); y+=40+bh+gap
    d.text((x,height-pad-180),
           "Use your strengths—and stretch one new mechanism—this week.",
           font=small_f,fill=(60,60,60))
    bio=io.BytesIO(); img.save(bio,"PNG",optimize=True); bio.seek(0); return bio

# ------------------------------------------------------------
# UI
# ------------------------------------------------------------
def scenario_ui(i):
    sc=SCENARIOS[i]
    st.markdown(f"### {sc['title']}"); st.caption(sc["context"])
    with st.expander("Why this matters",expanded=False): st.write(sc["why"])
    opts=[o for (o,_) in sc["opts"]]; prev=st.session_state.answers.get(i)
    default=opts.index(prev) if prev in opts else 0
    choice=st.radio("What would you most likely do?",opts,index=default,
                    label_visibility="collapsed",key=f"q_{i}")
    c1,c2=st.columns(2)
    if c1.button("◀ Back",disabled=(st.session_state.page==0),use_container_width=True):
        st.session_state.page-=1; st.rerun()
    if c2.button("Next ▶",use_container_width=True):
        st.session_state.answers[i]=choice; st.session_state.page+=1; st.rerun()

def results_ui():
    s=score_mechanisms(); st.success("🎉 You’ve completed your Boundary Compass journey.")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("I",s["I"]); c2.metric("C",s["C"]); c3.metric("R",s["R"]); c4.metric("T",s["T"])
    fig=go.Figure(go.Bar(x=[s["I"],s["C"],s["R"],s["T"]],
                         y=["I","C","R","T"],orientation="h",
                         marker=dict(color=[MECH_COLORS[k] for k in ["I","C","R","T"]])))
    fig.update_layout(height=320,margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig,use_container_width=True)
    code=pick_archetype(s); meta=ARCHETYPE_META[code]
    st.markdown(f"## {meta['name']}"); st.write(meta["desc"])
    for mech,_ in underused(s):
        st.write(f"**{mech}** — {MICRO_PRACTICES[mech]}")
    st.divider()
    st.write("**Reflection:** Which upcoming situation might test your Compass—and what small experiment will you try?**")
    card=generate_result_card(code,s)
    st.image(card,use_column_width=True,caption="Save or screenshot your result card.")
    st.download_button("⬇️ Download result card",data=card,
                       file_name="BoundaryCompass.png",mime="