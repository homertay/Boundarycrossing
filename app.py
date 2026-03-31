"""
MBX Boundary Crossing Diagnostic — SJT Edition v2
Master in Boundary-Crossing Learning and Leadership | IAL/SUSS

20 situational scenarios across 4 dimensions × 5 organisational levels.
Scenarios are sector-agnostic, wicked-problem framed, and capture
the experience of being pulled in multiple directions.
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

@st.cache_resource
def get_class_store():
    return []

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
# DIMENSIONS
# ─────────────────────────────────────────────────────────────────────────────
DIMENSIONS = {
    "awareness": {
        "name": "Boundary Awareness",
        "icon": "🔍",
        "color": "#2563EB",
        "tagline": "Noticing and naming the tensions that shape your work",
        "feedback": [
            "You tend to treat boundary signals as operational problems rather than relational or structural ones. The habit of pausing to ask 'what kind of problem is this, really?' can open up options that task-focused responses miss.",
            "You notice tensions in familiar contexts. The growth edge is naming them explicitly — even when doing so creates discomfort, slows things down, or makes you the person who complicates a situation others want to move past quickly.",
            "You have a well-developed capacity to identify and articulate the invisible lines shaping your work. Consider how you help others develop this awareness — naming boundaries is a leadership act, not just a personal skill.",
            "You notice boundaries early, name them precisely, and treat them as collective learning opportunities rather than individual inconveniences. This is a rare and high-value leadership capability in complex, ambiguous environments.",
        ],
    },
    "coordination": {
        "name": "Coordination",
        "icon": "🤝",
        "color": "#10B981",
        "tagline": "Building bridges, shared structures, and lasting routines",
        "feedback": [
            "You tend to coordinate through informal means — relationships, goodwill, and individual effort. These work until they don't. When the people who hold informal knowledge leave or are unavailable, coordination breaks down. Lightweight shared structures can make your team's work more resilient without adding bureaucracy.",
            "You create coordination fixes when friction becomes visible. The shift toward designing coordination proactively — before problems surface — is where significant capacity gains tend to come from.",
            "You build effective coordination structures and help others work through shared systems. Check that the structures you create are genuinely owned by the team rather than dependent on your continued involvement to function.",
            "You design coordination as infrastructure — systems, norms, and shared artefacts that outlast any individual and create the conditions for sustained cross-boundary work. You understand that the goal is a team that coordinates without you, not one that coordinates through you.",
        ],
    },
    "reflection": {
        "name": "Reflective Capacity",
        "icon": "🪞",
        "color": "#F59E0B",
        "tagline": "Learning about yourself through encounters with difference",
        "feedback": [
            "Boundary encounters carry information about your assumptions — but only if you examine them rather than explain them away. Even a short reflective pause after a difficult encounter can surface patterns that would otherwise remain invisible.",
            "You reflect when prompted or when something goes wrong. Building reflection into your regular rhythm — not just reactively — allows you to extract more learning from ordinary experience rather than waiting for things to break.",
            "You treat encounters with difference as genuine learning material and are willing to sit with uncomfortable questions about your own assumptions and patterns. This capacity for honest self-examination is a significant leadership strength.",
            "You treat your own reactions as data, share your reflections with others when it creates learning, and create conditions for collective sense-making. You understand that reflective leadership is not just about looking inward — it's about what you do with what you find.",
        ],
    },
    "transformation": {
        "name": "Transformative Practice",
        "icon": "✨",
        "color": "#8B5CF6",
        "tagline": "Generating new knowledge and practice through crossing",
        "feedback": [
            "Your boundary crossings may not yet be generating new practice. The question is not just 'how do I manage this tension?' but 'what could emerge here that didn't exist before?' That shift in frame is the first step toward transformative work.",
            "You occasionally generate new insights from boundary encounters. The next step is treating these insights as deliberately as you treat operational problems — scoping experiments, involving others, and creating conditions for what you've learned to travel.",
            "You actively create conditions for new practice to emerge. You know how to scope experiments, hold ambiguity, and document learning in ways that can be shared. Your challenge is ensuring that what you create doesn't stay within your immediate sphere.",
            "You are not just crossing boundaries — you are transforming practices on both sides. You treat every significant boundary encounter as a potential site of institutional learning, and you build the conditions for that learning to persist beyond you.",
        ],
    },
}

LEVEL_LABELS = {
    "systemic":   "🏛 Systemic",
    "team":       "👥 Team",
    "leader_sub": "🧑‍💼 Leader–Subordinate",
    "mindset":    "🧠 Individual Mindset",
    "technology": "💻 Technology",
}

# ─────────────────────────────────────────────────────────────────────────────
# 20 SJT SCENARIOS
# Options listed in randomised developmental order (not Emerging→Advanced)
# to reduce obvious gaming. Each option carries its score as metadata.
# ─────────────────────────────────────────────────────────────────────────────
SCENARIOS = [

    # ── BOUNDARY AWARENESS ──────────────────────────────────────────────────

    {
        "id": "A1", "dim": "awareness", "level": "systemic",
        "title": "The Merge That Wasn't",
        "context": (
            "Your organisation recently brought two previously separate teams under your management. "
            "On paper, integration is complete. In practice, the teams operate as if they are still separate — "
            "different rhythms, different assumptions about what good work looks like, quiet loyalties to the old structure. "
            "You are expected to show that the integration is working. "
            "Leadership has moved on. The teams haven't."
        ),
        "prompt": "You are pulled between demonstrating progress and addressing what you're actually seeing. What do you do?",
        "options": [
            ("Focus on outputs and deliverables — cultural integration takes time and cannot be rushed or forced.", 1),
            ("Notice the division but wait for a natural opportunity to address it without creating disruption.", 2),
            ("Name the dynamic explicitly with both groups: 'We're technically one team but operating as two — I think that's worth examining together.'", 3),
            ("Facilitate a structured integration process — surfacing the different working assumptions, identifying where they create friction, and co-designing what a genuinely shared team culture would look like.", 4),
        ],
    },
    {
        "id": "A2", "dim": "awareness", "level": "team",
        "title": "The Same Goal, Different Games",
        "context": (
            "Your project team has been working together for three months. On the surface, everyone is aligned. "
            "Underneath, you notice each person is optimising for something slightly different — "
            "some for speed, some for quality, some for how the work reflects on their own team, some for their manager's priorities. "
            "No one has said any of this aloud. The team appears collaborative but moves slowly. "
            "When things stall, each person has a different explanation for why."
        ),
        "prompt": "Naming this risks making people defensive. Not naming it means the friction continues. What do you do?",
        "options": [
            ("Name what you observe in a team session: 'I think we might be optimising for different things without realising it — can we make that visible?'", 3),
            ("Keep moving — teams working on complex problems naturally find alignment as the deadline focuses minds.", 1),
            ("Have quiet individual conversations with the people you trust most to understand what's really going on.", 2),
            ("Facilitate a structured conversation to map each person's actual success criteria, surface the tensions, and renegotiate shared priorities before the friction compounds.", 4),
        ],
    },
    {
        "id": "A3", "dim": "awareness", "level": "leader_sub",
        "title": "The Brief That Was Never Enough",
        "context": (
            "A capable team member consistently delivers work that meets every explicit requirement "
            "but misses what the context actually demands — the political undercurrents, the unstated expectations, "
            "the real concerns of the people the work is for. "
            "When you give feedback, they are genuinely confused. From where they stand, they did exactly what was asked. "
            "You can feel the gap but struggle to articulate it precisely. "
            "And you wonder whether the problem is theirs, yours, or somewhere in between."
        ),
        "prompt": "The feedback feels like moving goalposts to them, and maybe it is. What do you do?",
        "options": [
            ("Treat this as a communication problem and be more explicit in briefs going forward.", 1),
            ("Acknowledge to yourself that there is a gap in how you each read the work, but assume it will narrow with experience.", 2),
            ("Have a direct conversation about the unspoken expectations you carry — naming what has been implicit and examining whether those expectations are reasonable to hold unstated.", 3),
            ("Treat this as a boundary worth examining together — discuss the different mental models you each bring to the work, and co-create a shared framework for what 'reading the context' actually requires.", 4),
        ],
    },
    {
        "id": "A4", "dim": "awareness", "level": "mindset",
        "title": "The Frustration You Keep Explaining Away",
        "context": (
            "You leave a recurring cross-team meeting feeling a familiar low-grade frustration. "
            "The right things are being reported. Progress is visible. The room is professionally cordial. "
            "But something consistently feels off — like the real issues are being managed around rather than addressed. "
            "Later, you find yourself wondering whether the problem is the meeting format, the other people, "
            "or something you're not doing, not saying, or not seeing in yourself."
        ),
        "prompt": "It's easier to attribute the feeling to external causes. What do you do?",
        "options": [
            ("Accept the frustration as a normal feature of cross-functional work — some meetings are just like this.", 1),
            ("Acknowledge the frustration privately and decide to raise the meeting format at an appropriate moment.", 2),
            ("Sit with the discomfort long enough to examine your own role — what are you avoiding saying, and what might you be contributing to the dynamic you're frustrated by?", 3),
            ("Use the experience as diagnostic data — examine your own reactions, discuss with a trusted peer, and consider what the pattern might reveal about assumptions you carry into that room.", 4),
        ],
    },
    {
        "id": "A5", "dim": "awareness", "level": "technology",
        "title": "The Tool You Keep Overruling",
        "context": (
            "Your organisation has invested in a system that surfaces patterns and anomalies your team "
            "would not typically generate on their own. Six months in, you notice the team consistently "
            "sets aside its outputs — sometimes for good contextual reasons, sometimes reflexively, "
            "and sometimes, you suspect, because the outputs are uncomfortable. "
            "The boundary between legitimate professional judgment and defensive habit "
            "is not clear, and no one has tried to draw it."
        ),
        "prompt": "Both the tool and your team's judgment have real value. What do you do?",
        "options": [
            ("Trust the team — they have contextual knowledge the tool doesn't, and second-guessing them undermines confidence.", 1),
            ("Encourage the team to engage more thoughtfully with the outputs, but leave it to their discretion.", 2),
            ("Name the pattern explicitly: 'I notice we consistently set aside the tool's outputs — I'd like us to examine whether we're making deliberate judgments or forming a habit of dismissal.'", 3),
            ("Facilitate a structured review of recent cases where the tool was overridden — asking the team to articulate their reasoning and using this to surface the unexamined assumptions about expertise, risk, and what counts as reliable knowledge.", 4),
        ],
    },

    # ── COORDINATION ─────────────────────────────────────────────────────────

    {
        "id": "C1", "dim": "coordination", "level": "systemic",
        "title": "No One's Problem, Everyone's Problem",
        "context": (
            "You are co-leading a significant initiative with a peer from another part of the organisation. "
            "Both of you have partial authority, complementary expertise, and completely different teams, "
            "timelines, and reporting lines. "
            "The work keeps stalling at the points where your domains meet — "
            "not because of conflict, but because neither of you is sure whose call it is. "
            "Both of you are too stretched to resolve it cleanly. "
            "Escalating feels like admitting failure. Continuing without resolving it is slowly killing the project."
        ),
        "prompt": "You are pulled between momentum and clarity. What do you do?",
        "options": [
            ("Keep moving and resolve ambiguities case by case — escalating ownership questions creates more problems than it solves.", 1),
            ("Raise the issue with your peer informally and agree to check in more frequently on the friction points.", 2),
            ("Design a simple shared structure — clear decision rights, a brief joint escalation path, and a regular rhythm for surfacing issues before they stall the work.", 3),
            ("Treat the coordination failure as a design problem — co-create a governance structure that both teams understand, that clarifies who owns what, and that creates visible mechanisms for resolving ambiguity without escalating every time.", 4),
        ],
    },
    {
        "id": "C2", "dim": "coordination", "level": "team",
        "title": "The Meeting That Has Become Theatre",
        "context": (
            "Your team meets regularly. Updates are shared. Actions are logged. "
            "The same issues reappear at the next meeting in slightly different form. "
            "Real decisions happen in corridors, in direct messages, in conversations you're not in. "
            "The formal meeting has become a place where things are reported rather than resolved. "
            "Everyone is polite. No one has named what is happening. "
            "You are not sure whether naming it would help or make things worse."
        ),
        "prompt": "The dysfunction is functional enough that no one is demanding change. What do you do?",
        "options": [
            ("Continue as is — the informal channels are actually working, and disrupting the formal structure risks the whole system.", 1),
            ("Restructure the agenda to focus on decisions rather than updates and see whether that shifts the dynamic.", 2),
            ("Name the pattern directly with the team: 'I think our meetings have become more about reporting than resolving — I'd like to change that, and I'd like your help designing something better.'", 3),
            ("Facilitate a genuine conversation about what coordination actually requires in your current context — then co-design a new structure, including explicit norms about where decisions should happen and how the informal network connects to the formal one.", 4),
        ],
    },
    {
        "id": "C3", "dim": "coordination", "level": "leader_sub",
        "title": "The Knowledge No One Else Has",
        "context": (
            "The most important knowledge in your team — who to go to, what the real constraints are, "
            "how to read the key people, which battles are worth fighting — "
            "lives in your head and in a small number of informal relationships. "
            "It works. You get things done others can't. "
            "But you've started noticing that when you're unavailable, things slow to a halt. "
            "Newer team members can't navigate independently. "
            "You are, without intending it, a bottleneck."
        ),
        "prompt": "Your knowledge is a source of genuine value. Making it explicit changes your role. What do you do?",
        "options": [
            ("Continue as is — this kind of knowledge can't really be documented, and the relationships took years to build.", 1),
            ("Brief a deputy more comprehensively so the team can function when you're not available.", 2),
            ("Begin systematically externalising the knowledge — documenting key relationships, context, and judgment calls in shared formats the team can access and build on.", 3),
            ("Treat this as a structural problem worth redesigning — map what knowledge exists where, who needs it, and co-create a system that distributes context and decision-making capacity across the team rather than concentrating it in you.", 4),
        ],
    },
    {
        "id": "C4", "dim": "coordination", "level": "mindset",
        "title": "The Coordinator Who Can't Be Absent",
        "context": (
            "You have built your effectiveness on knowing the right people and being trusted across teams. "
            "You get things done that others cannot because of relationship capital accumulated over years. "
            "But the same quality that makes you effective also means that "
            "when you are not in the room, the connections don't hold. "
            "You've started to wonder whether you have built a team that works through you "
            "rather than one that works without you — and whether that distinction matters."
        ),
        "prompt": "The relationship approach is genuinely valuable and genuinely limiting. What do you do?",
        "options": [
            ("Continue as is — relationship-based coordination is a real leadership skill, and the team values what you bring.", 1),
            ("Introduce more structure to the most critical coordination points so the team is less dependent on your personal involvement.", 2),
            ("Reflect honestly on which coordination tasks rely on your personal relationships and begin building shared processes that could work without you at the centre.", 3),
            ("Treat your own effectiveness as a design problem — map your relational capital, understand what the team can and cannot do without you, and deliberately build their coordination capacity as a leadership priority.", 4),
        ],
    },
    {
        "id": "C5", "dim": "coordination", "level": "technology",
        "title": "Everything Is Somewhere",
        "context": (
            "Your team has accumulated a patchwork of tools, drives, channels, and trackers "
            "— each introduced to solve a specific problem, none of them integrated. "
            "Information is duplicated across platforms. "
            "Decisions made in one channel are invisible to people in another. "
            "New members spend weeks just working out where things live. "
            "Everyone acknowledges it is a problem. "
            "No one has the time, authority, or appetite to fix it properly — "
            "and every partial fix has historically made things slightly more complicated."
        ),
        "prompt": "The system is broken in a way that feels too embedded to change. What do you do?",
        "options": [
            ("Let individuals use whatever tools work for them — trying to standardise creates resistance and makes you responsible for a system no one will maintain.", 1),
            ("Propose a simpler setup and encourage the team to migrate, but don't mandate it.", 2),
            ("Facilitate a team audit of current tool usage and co-design a clear technology charter: which tool serves which purpose, and how the team will maintain the agreement.", 3),
            ("Treat the tool sprawl as a symptom of a coordination design problem — map the actual workflows, identify where information needs to flow, design the simplest possible system that serves those needs, and build in a regular review so the system evolves rather than accumulates.", 4),
        ],
    },

    # ── REFLECTIVE CAPACITY ──────────────────────────────────────────────────

    {
        "id": "R1", "dim": "reflection", "level": "systemic",
        "title": "Between Loyalty and What You Actually Think",
        "context": (
            "A significant strategic decision has been made above you that you are now expected to implement and advocate for. "
            "You have real reservations — not because you think it is simply wrong, "
            "but because you can see consequences that may not have been fully considered, "
            "and the people most affected had the least voice in the decision. "
            "You are being pulled between institutional loyalty, personal integrity, "
            "and your responsibility to the people you lead. "
            "There is no clean option."
        ),
        "prompt": "Speaking up has costs. Staying silent has different costs. What do you do?",
        "options": [
            ("Implement as directed — it is not your role to second-guess decisions made above you, and visible reservation undermines the organisation.", 1),
            ("Implement while noting your reservations privately and monitoring what happens.", 2),
            ("Implement while raising your concerns through the appropriate channels — documenting your perspective clearly and ensuring the people most affected have some form of voice in the process.", 3),
            ("Implement with integrity — facilitate a conversation with your team about what it means to carry out a decision you have reservations about, surface the tensions honestly, and create structured mechanisms to feed back what you observe to the decision-makers.", 4),
        ],
    },
    {
        "id": "R2", "dim": "reflection", "level": "team",
        "title": "The Gap Between Intention and Impact",
        "context": (
            "After a demanding period of work, informal feedback reaches you that your team experienced "
            "your leadership as controlling — that they felt directed rather than trusted, managed rather than developed. "
            "Your own experience of that period was of holding things together under significant pressure. "
            "You believed you were protecting the team. "
            "They experienced something different. "
            "The gap between your intention and their experience is wider than you knew, "
            "and you are not entirely sure what to do with that."
        ),
        "prompt": "The defensive impulse is strong. The feedback may be partly unfair. It may also be true. What do you do?",
        "options": [
            ("Note the feedback and attribute it to the pressure of the period — you know what that situation required and would make the same calls again.", 1),
            ("Reflect privately and resolve to give the team more autonomy when conditions allow.", 2),
            ("Follow up with the people who gave feedback — ask for specific examples, share your own account of the period, and try to understand the gap between what you intended and what they experienced.", 3),
            ("Create a structured debrief with the team — share what you heard without defensiveness, own the impact regardless of intention, explore the gap honestly, and co-design what you want the working relationship to look like going forward.", 4),
        ],
    },
    {
        "id": "R3", "dim": "reflection", "level": "leader_sub",
        "title": "What the Departure Revealed",
        "context": (
            "Someone you valued highly has decided to leave. "
            "In the conversation before they go, they tell you something honest you weren't expecting: "
            "that they stopped growing under you — that you consistently gave them work they were already good at "
            "rather than work that would stretch them. "
            "You believed you were deploying them well. They experienced being held in place. "
            "You can't act on this feedback — they're leaving. "
            "But you find yourself wondering how many other people on your team feel the same way "
            "and haven't said anything."
        ),
        "prompt": "The feedback is too late to act on for this person. What do you do with it?",
        "options": [
            ("Accept it graciously and note it for future reference — every manager has blind spots and this was one of yours.", 1),
            ("Reflect on whether you relied on this person too heavily and resolve to be more deliberate about development conversations with the team.", 2),
            ("Sit with the discomfort — examine your assumptions about what development actually means, and whether you have been prioritising team stability, your own comfort, or what was genuinely best for the individuals.", 3),
            ("Use this as a catalyst for genuine inquiry — have development conversations with your current team members, examine your own defaults around stretch versus safety, and ask yourself what you would need to change about how you lead for people to grow.", 4),
        ],
    },
    {
        "id": "R4", "dim": "reflection", "level": "mindset",
        "title": "The Voice You Keep Not Using",
        "context": (
            "In rooms with senior or influential people, you consistently hold back. "
            "You soften your actual view, hedge your assessment, wait for someone else to say what you're thinking. "
            "Afterwards, you often leave with the thought that you should have said more. "
            "The pattern is familiar — it has been present for years. "
            "You have explanations for it: reading the room, professional judgment, picking battles, respecting hierarchy. "
            "Some of those explanations feel true. "
            "But something about the pattern still troubles you, "
            "and you notice it is costing you in ways you haven't fully named."
        ),
        "prompt": "The explanations feel real but the pattern continues. What do you do?",
        "options": [
            ("Continue exercising professional judgment about when to speak — the pattern reflects contextual intelligence, not a problem.", 1),
            ("Acknowledge the pattern privately and look for lower-stakes opportunities to practise speaking more directly.", 2),
            ("Examine the assumptions underneath the pattern — what exactly are you afraid of, when does deference serve the work and when does it protect you, and what is the cost of staying silent?", 3),
            ("Treat this as a genuine leadership edge — explore the roots of the pattern with a coach or trusted peer, practise deliberately in situations that feel safe enough to stretch, and build a personal strategy for navigating the tension between voice and deference.", 4),
        ],
    },
    {
        "id": "R5", "dim": "reflection", "level": "technology",
        "title": "When the Tool Does It Better",
        "context": (
            "Your team has integrated an AI tool into a core workflow. "
            "The outputs are often strong — sometimes stronger than what the team would produce independently. "
            "Review processes have become more cursory. "
            "People are beginning to trust the tool's judgment over their own in certain situations. "
            "You feel a professional unease you are struggling to articulate precisely. "
            "It isn't that the tool is wrong. "
            "It's something about the direction of the dependency, "
            "and what it might be quietly doing to the team's capacity to think."
        ),
        "prompt": "The tool is genuinely useful. The unease is real but hard to name. What do you do?",
        "options": [
            ("Accept this as a natural feature of good tool adoption — if the outputs are strong, lighter review is efficient, not a problem.", 1),
            ("Mention to the team that they should stay engaged with the outputs critically, without making it a bigger issue.", 2),
            ("Name your unease explicitly and open a conversation: 'I want to examine what it means for our professional judgment and accountability when a tool consistently produces work we would be proud to have done ourselves.'", 3),
            ("Facilitate a genuine team inquiry — what does the tool change about how you think, what you're responsible for, and what expertise means in your context? Develop a shared position on what good human–AI collaboration looks like for your team specifically.", 4),
        ],
    },

    # ── TRANSFORMATIVE PRACTICE ──────────────────────────────────────────────

    {
        "id": "T1", "dim": "transformation", "level": "systemic",
        "title": "The Group That Produces Nothing New",
        "context": (
            "You sit on a cross-organisational working group that has existed for two years. "
            "Meetings are well-attended. Reports are produced. "
            "Both organisations use participation in the group to demonstrate collaboration "
            "without being genuinely changed by it. "
            "Real decisions happen elsewhere. "
            "The group's continued existence may be preventing more honest conversations "
            "about why the deeper collaboration isn't happening. "
            "No one else seems willing to name this. "
            "And naming it has costs."
        ),
        "prompt": "Staying costs something. Disrupting it costs something else. What do you do?",
        "options": [
            ("Continue participating — institutional structures like this are slow to change and leaving would remove any chance of influence.", 1),
            ("Raise the question of the group's effectiveness at the next meeting and propose a mandate review.", 2),
            ("Propose a fundamental shift in what the group does — from reporting to genuine joint problem-solving, with a specific shared challenge as the test case.", 3),
            ("Facilitate a reckoning with what the group is actually for — name the performance openly, invite an honest conversation about what genuine collaboration would require from both sides, and redesign from that honesty rather than around it.", 4),
        ],
    },
    {
        "id": "T2", "dim": "transformation", "level": "team",
        "title": "The Better Way No One Else Knows",
        "context": (
            "Over eighteen months of iteration and learning from failure, "
            "your team has developed a significantly better approach to a recurring challenge. "
            "It works. The evidence is clear. "
            "But it exists only within your team. "
            "You haven't documented it, shared it, or tried to spread it. "
            "Partly because you're busy. Partly because you're not sure others would value it. "
            "And partly — if you're honest — because it has become part of what makes your team distinctive, "
            "and you're not certain you want to give that away."
        ),
        "prompt": "Sharing it changes your team's position. Not sharing it keeps a gap between knowing and doing. What do you do?",
        "options": [
            ("Continue as is — the approach took years to develop, and it's not your responsibility to do others' learning for them.", 1),
            ("Mention it to peers informally and let genuine interest develop naturally before investing in any formal sharing.", 2),
            ("Document the approach clearly and share it with leadership, proposing a structured pilot with one other team.", 3),
            ("Treat what you've built as a shared resource — create a transferable version of the methodology, run a cross-team learning session, and actively help others adapt it to their contexts, including being honest about the eighteen months of failure that preceded success.", 4),
        ],
    },
    {
        "id": "T3", "dim": "transformation", "level": "leader_sub",
        "title": "The Idea You Almost Dismissed",
        "context": (
            "A team member brings you an unconventional proposal for a problem your organisation "
            "has been circling for years without resolving. "
            "The idea sits outside standard parameters. "
            "Your first instinct is to explain the obstacles — the process, the timing, the risk. "
            "The instinct comes quickly. "
            "But something about the idea is more interesting than the instinct wants to acknowledge, "
            "and you notice you're not entirely sure whether your caution is protecting the team member "
            "or protecting yourself."
        ),
        "prompt": "The idea may be worth more than your first instinct suggests. What do you do?",
        "options": [
            ("Thank them for the thinking and redirect their energy toward more viable approaches — protecting them from a costly, demoralising failure is part of your job.", 1),
            ("Explore the idea with them informally and be honest about the obstacles, leaving it to them to decide whether to pursue it.", 2),
            ("Work with them to scope a low-risk version of the proposal — small enough to test the core idea without requiring approval for the full thing.", 3),
            ("Treat this as a leadership opportunity — sit with your own first instinct long enough to examine it, co-develop the proposal seriously, coach them through the organisational landscape, and create conditions for a genuine test regardless of what you predict the outcome to be.", 4),
        ],
    },
    {
        "id": "T4", "dim": "transformation", "level": "mindset",
        "title": "The Expert Who Must Become Something Else",
        "context": (
            "You built your career and your credibility on knowing more than others in your domain — "
            "being the person with the answer, the one who sets direction, the one others come to. "
            "Your current role requires something different: "
            "facilitating rather than directing, creating conditions for others to think, "
            "being genuinely comfortable with outcomes you didn't design. "
            "The shift is harder than you expected. "
            "And you are not always sure whether the moments you reach for the expert role "
            "are genuinely necessary or a way of managing your own discomfort with the uncertainty."
        ),
        "prompt": "Your expertise is real. So is the discomfort. What do you do?",
        "options": [
            ("Lead from expertise — it is what your team expects and what you are genuinely best at, and this version of 'facilitative leadership' is often just less effective leadership.", 1),
            ("Try facilitative approaches in some situations while defaulting to direction when pressure is high or the stakes are significant.", 2),
            ("Name the shift explicitly — with yourself and your team — and experiment deliberately with facilitative approaches, tracking what you learn about your own range and what the team is capable of when you get out of the way.", 3),
            ("Treat the discomfort as a developmental signal worth taking seriously — design a sustained personal experiment with real reflection built in (journalling, peer coaching, supervision), and commit to examining the patterns honestly enough to change them.", 4),
        ],
    },
    {
        "id": "T5", "dim": "transformation", "level": "technology",
        "title": "Not Faster — Different",
        "context": (
            "Working with AI tools over the past months, you've started to see that "
            "the real potential is not efficiency — doing the same things faster — "
            "but something more fundamental: "
            "a genuinely different way of approaching problems, distributing thinking, "
            "and organising how work gets done. "
            "Realising that potential would require your team to change not just their tools "
            "but their assumptions about their own roles, expertise, and what good work looks like. "
            "That is a much harder conversation than 'here's a useful tool.' "
            "And you're not sure your organisation — or you — is ready for it."
        ),
        "prompt": "The incremental path is safer. The transformative path is uncertain. What do you do?",
        "options": [
            ("Continue incremental adoption — change carries risk, and the efficiency gains from current use already justify the investment.", 1),
            ("Share your emerging perspective with your team and gauge their appetite for a more fundamental rethink before committing to anything.", 2),
            ("Design a structured experiment — scope a specific workflow for reimagining, define what success looks like beyond efficiency, and run a real pilot with a learning design built in.", 3),
            ("Treat this as a moment that requires genuine co-creation — involve the team in examining their assumptions about work and expertise, not just in adopting a new tool, and build a shared learning architecture that can evolve as the technology and the team's understanding evolves together.", 4),
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────────────────────────────────────
def compute_scores(answers: dict) -> dict:
    totals = {k: 0 for k in DIMENSIONS}
    for sc in SCENARIOS:
        val = answers.get(sc["id"])
        if val is not None:
            totals[sc["dim"]] += val
    return totals

def score_tier(s: float, max_s: float = 20):
    pct = s / max_s
    if pct < 0.40: return "Emerging",   "#F97316", 0
    if pct < 0.60: return "Developing", "#3B82F6", 1
    if pct < 0.80: return "Proficient", "#10B981", 2
    return              "Advanced",   "#8B5CF6", 3

# ─────────────────────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────────────────────
def make_radar(all_scores, labels, title="Boundary Crossing Profile"):
    keys   = list(DIMENSIONS.keys())
    names  = [DIMENSIONS[k]["name"] for k in keys]
    pal    = ["#2563EB","#F59E0B","#10B981","#8B5CF6","#EF4444"]
    fig    = go.Figure()
    for i, scores in enumerate(all_scores):
        vals  = [scores[k] for k in keys] + [scores[keys[0]]]
        theta = names + [names[0]]
        c     = pal[i % len(pal)]
        r,g,b = int(c[1:3],16), int(c[3:5],16), int(c[5:7],16)
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=theta, fill="toself",
            fillcolor=f"rgba({r},{g},{b},0.12)",
            line=dict(color=c, width=2.5), name=labels[i],
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(248,250,252,0.9)",
            radialaxis=dict(visible=True, range=[0,20], tickvals=[5,10,15,20],
                            tickfont=dict(size=10,color="#94A3B8"),
                            gridcolor="rgba(148,163,184,0.25)",
                            linecolor="rgba(148,163,184,0.25)"),
            angularaxis=dict(gridcolor="rgba(148,163,184,0.2)",
                             tickfont=dict(size=12,color="#334155")),
        ),
        showlegend=len(all_scores)>1, legend=dict(font=dict(size=11)),
        title=dict(text=title, font=dict(size=14,color="#1E293B",family="Georgia,serif"), x=0.5),
        paper_bgcolor="white", plot_bgcolor="white",
        height=400, margin=dict(t=65,b=10,l=20,r=20),
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
        text=[f"{v}/20" for v in vals], textposition="outside",
        textfont=dict(size=12, color="#1E293B"),
    ))
    fig.update_layout(
        height=240,
        xaxis=dict(range=[0,24], showgrid=True, gridcolor="#E2E8F0",
                   tickfont=dict(color="#94A3B8",size=10), zeroline=False),
        yaxis=dict(tickfont=dict(size=12,color="#334155")),
        paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(t=10,b=10,l=10,r=50), showlegend=False,
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
        s              = scores[key]
        label, lc, ti  = score_tier(s)
        pct            = (s/20)*100
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
          <p style="margin:0;font-size:0.88rem;color:#475569;line-height:1.75">{dim['feedback'][ti]}</p>
        </div>"""
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Boundary Crossing Diagnostic — {name}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;700&family=DM+Sans:wght@400;500;600&display=swap');
  body{{font-family:'DM Sans',sans-serif;max-width:680px;margin:40px auto;padding:0 24px;color:#1E293B;background:#F8FAFC}}
  .hdr{{background:linear-gradient(135deg,#0F172A,#1E3A8A,#2563EB);border-radius:16px;padding:2.2rem 2rem;color:white;margin-bottom:1.5rem}}
  .hdr .lbl{{font-size:0.62rem;letter-spacing:3px;text-transform:uppercase;opacity:0.6;margin-bottom:0.6rem}}
  .hdr h1{{margin:0;font-size:1.7rem;font-family:'Lora',Georgia,serif;font-weight:700}}
  .hdr .meta{{margin:8px 0 0;opacity:0.8;font-size:0.88rem}}
  .reflect{{background:#EFF6FF;border-left:4px solid #2563EB;border-radius:8px;padding:1.1rem 1.3rem;margin:1.25rem 0}}
  .reflect h3{{margin:0 0 0.5rem;color:#1D4ED8;font-size:0.88rem;text-transform:uppercase;letter-spacing:1px}}
  .reflect p{{margin:0;color:#475569;font-size:0.9rem;line-height:1.75;font-style:italic}}
  .footer{{text-align:center;font-size:0.78rem;color:#CBD5E1;margin-top:2rem;padding-top:1rem;border-top:1px solid #E2E8F0}}
</style></head><body>
  <div class="hdr">
    <div class="lbl">MBX · Boundary-Crossing Learning and Leadership · IAL/SUSS</div>
    <h1>🔀 Boundary Crossing Diagnostic</h1>
    <div class="meta">{meta}</div>
  </div>
  <p style="color:#475569;font-size:0.9rem;line-height:1.75;margin-bottom:1.25rem">
    Based on your responses to 20 situational scenarios across five organisational levels 
    (systemic, team, leader–subordinate, individual mindset, and technology). 
    Scores reflect developmental tendencies, not fixed traits — and are most useful 
    as a starting point for reflection rather than a final verdict.
  </p>
  {rows}
  <div class="reflect">
    <h3>💭 Reflection Prompt</h3>
    <p>Which dimension surprised you — either higher or lower than you expected? 
    Looking at your lowest dimension: which of the five organisational levels 
    felt most difficult in the scenarios? What does that tell you about 
    where crossing boundaries is hardest in your current role and context?
    What is one specific tension you have been managing around rather than attending to?</p>
  </div>
  <div class="footer">MBX Boundary Crossing Diagnostic · IAL/SUSS · {now}<br>
    Inspired by Akkerman &amp; Bakker (2011).</div>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
def apply_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.main{background:#F8FAFC;}
.block-container{padding-top:1.5rem!important;max-width:720px!important;padding-bottom:3rem!important;}
#MainMenu,header,footer{visibility:hidden;}
.hero{background:linear-gradient(135deg,#0F172A 0%,#1E3A8A 55%,#2563EB 100%);
      border-radius:18px;padding:2.6rem 2.2rem;color:white;margin-bottom:1.5rem;
      text-align:center;position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;top:-60%;right:-15%;width:320px;height:320px;
              background:rgba(255,255,255,0.03);border-radius:50%;}
.hero-label{font-size:0.62rem;letter-spacing:3px;text-transform:uppercase;opacity:0.6;margin-bottom:0.8rem;}
.hero h1{font-family:'Lora',Georgia,serif;font-size:2rem;font-weight:700;margin:0;line-height:1.2;}
.hero p{font-size:0.92rem;opacity:0.8;margin:0.85rem auto 0;line-height:1.65;max-width:500px;}
.card{background:white;border-radius:14px;padding:1.3rem 1.5rem;margin-bottom:1rem;
      box-shadow:0 1px 6px rgba(15,23,42,0.07);border:1px solid rgba(226,232,240,0.8);}
.sc-level{font-size:0.72rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
          color:#94A3B8;margin-bottom:0.4rem;}
.sc-title{font-family:'Lora',Georgia,serif;font-size:1.1rem;font-weight:700;color:#1E293B;margin-bottom:0.5rem;}
.sc-context{font-size:0.91rem;color:#475569;line-height:1.8;}
.sc-prompt{font-size:0.86rem;font-weight:600;color:#1E293B;
           border-left:3px solid #2563EB;padding-left:0.75rem;margin:0.85rem 0 0.6rem;
           font-style:italic;}
.prog-wrap{margin-bottom:1.25rem;}
.prog-label{display:flex;justify-content:space-between;font-size:0.78rem;color:#64748B;margin-bottom:5px;}
.prog-bg{background:#E2E8F0;border-radius:999px;height:5px;}
.prog-fill{height:5px;border-radius:999px;background:linear-gradient(90deg,#1E40AF,#3B82F6);}
.r-card{background:white;border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:0.85rem;
        box-shadow:0 2px 8px rgba(15,23,42,0.07);border:1px solid rgba(226,232,240,0.8);}
.r-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;}
.r-name{font-weight:700;font-size:1rem;color:#1E293B;}
.r-tagline{font-size:0.78rem;color:#94A3B8;margin-top:3px;font-style:italic;}
.r-badge{color:white;padding:3px 12px;border-radius:999px;font-size:0.71rem;font-weight:700;
         letter-spacing:0.5px;white-space:nowrap;}
.r-score{font-family:'Lora',Georgia,serif;font-size:2rem;font-weight:700;color:#1E293B;
         margin-bottom:5px;line-height:1;}
.r-score span{font-family:'DM Sans',sans-serif;font-size:1rem;font-weight:400;color:#94A3B8;}
.r-bar-bg{background:#E2E8F0;border-radius:999px;height:6px;margin-bottom:0.85rem;}
.r-bar-fill{height:6px;border-radius:999px;}
.level-pills{display:flex;gap:0.4rem;flex-wrap:wrap;margin-bottom:0.85rem;}
.pill{background:#F1F5F9;border-radius:6px;padding:3px 10px;font-size:0.72rem;font-weight:600;color:#475569;}
.pill.best{background:#D1FAE5;color:#065F46;}
.pill.low{background:#FEF3C7;color:#92400E;}
.r-text{font-size:0.88rem;color:#475569;line-height:1.8;margin:0;}
.reflect-box{background:#EFF6FF;border-left:4px solid #2563EB;border-radius:10px;
             padding:1.1rem 1.4rem;margin:1.25rem 0;}
.reflect-title{font-weight:700;color:#1D4ED8;font-size:0.85rem;margin-bottom:0.5rem;}
.reflect-text{font-size:0.9rem;color:#475569;line-height:1.8;margin:0;font-style:italic;}
.confirm-box{background:linear-gradient(135deg,#064E3B,#059669);border-radius:14px;
             padding:1.5rem 2rem;color:white;text-align:center;margin:1rem 0;}
.confirm-box h3{margin:0 0 0.4rem;font-size:1.1rem;}
.confirm-box p{margin:0;opacity:0.85;font-size:0.88rem;}
.stButton>button{background:linear-gradient(135deg,#1E3A8A,#2563EB)!important;
    color:white!important;border:none!important;border-radius:10px!important;
    padding:0.62rem 1.5rem!important;font-weight:600!important;font-size:0.93rem!important;
    width:100%!important;font-family:'DM Sans',sans-serif!important;transition:all 0.2s!important;}
.stButton>button:hover{transform:translateY(-1px)!important;box-shadow:0 6px 18px rgba(37,99,235,0.3)!important;}
div[data-testid="stRadio"]>label{display:none!important;}
div[data-testid="stRadio"] div[role="radiogroup"]{flex-direction:column!important;gap:0.5rem!important;}
div[data-testid="stRadio"] div[role="radiogroup"] label{
    background:#F8FAFC;border-radius:10px;padding:0.75rem 1rem!important;
    font-size:0.9rem!important;color:#334155!important;
    border:1.5px solid #E2E8F0;transition:all 0.15s;cursor:pointer;width:100%;}
div[data-testid="stRadio"] div[role="radiogroup"] label:hover{background:#EFF6FF;border-color:#93C5FD;}
div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked){
    background:#EFF6FF;border-color:#2563EB;color:#1D4ED8!important;font-weight:600;}
.stTextInput>div>div>input{border-radius:10px!important;border:1.5px solid #E2E8F0!important;
    font-family:'DM Sans',sans-serif!important;font-size:0.95rem!important;
    padding:0.6rem 1rem!important;background:white!important;}
.stTextInput>div>div>input:focus{border-color:#2563EB!important;box-shadow:0 0 0 3px rgba(37,99,235,0.1)!important;}
section[data-testid="stSidebar"]{background:#0F172A!important;}
section[data-testid="stSidebar"] *{color:white!important;}
section[data-testid="stSidebar"] .stTextInput>div>div>input{
    background:rgba(255,255,255,0.1)!important;border-color:rgba(255,255,255,0.2)!important;color:white!important;}
details{border-radius:10px!important;background:white!important;border:1px solid #E2E8F0!important;}
</style>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "welcome", "q_idx": 0, "order": None,
        "answers": {}, "opt_orders": {},
        "name": "", "class_code": "",
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
2. **Extensions → Apps Script** → paste:

```javascript
function doPost(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheets()[0];
  var d  = JSON.parse(e.postData.contents);
  if (sh.getLastRow() === 0) sh.appendRow(Object.keys(d));
  sh.appendRow(Object.values(d));
  return ContentService.createTextOutput("ok");
}
```

3. **Deploy → New deployment → Web app**  
   Execute as: Me · Access: Anyone → Copy URL

4. In Streamlit Cloud → app **Settings → Secrets**:
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
        st.info("📭 No submissions yet.")
        return
    st.metric("Participants submitted", len(store))
    keys = list(DIMENSIONS.keys())
    all_s = [r["scores"] for r in store]
    avg   = {k: round(sum(s[k] for s in all_s)/len(all_s),1) for k in keys}
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(make_radar([avg],["Class Average"],"Class Average"), use_container_width=True)
    with col2:
        labels = [r["name"].split()[0] for r in store]
        st.plotly_chart(make_radar(all_s, labels, "All Participants"), use_container_width=True)
    st.markdown("#### Individual Scores")
    rows = []
    for r in store:
        row = {"Name": r["name"], "Time": r["timestamp"]}
        for k in keys:
            row[DIMENSIONS[k]["name"]] = f"{r['scores'][k]}/20"
        row["Class Code"] = r.get("class_code","—")
        rows.append(row)
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("📥 Download CSV", data=df.to_csv(index=False),
                       file_name=f"mbx_diagnostic_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                       mime="text/csv")
    st.markdown("---")
    st.markdown("#### 💬 Debrief Starters")
    sd = sorted(keys, key=lambda k: avg[k])
    lo, hi = DIMENSIONS[sd[0]], DIMENSIONS[sd[-1]]
    st.markdown(f"""
    <div style="background:#F0FDF4;border-left:4px solid #10B981;border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.75rem">
      <strong>Collective strength: {hi['icon']} {hi['name']} ({avg[sd[-1]]:.1f}/20)</strong><br>
      <span style="font-size:0.9rem;color:#475569">What has your collective context rewarded or required that has developed this?
      Where might it be creating blind spots?</span>
    </div>
    <div style="background:#FFF7ED;border-left:4px solid #F59E0B;border-radius:10px;padding:1rem 1.2rem;margin-bottom:0.75rem">
      <strong>Collective growth edge: {lo['icon']} {lo['name']} ({avg[sd[0]]:.1f}/20)</strong><br>
      <span style="font-size:0.9rem;color:#475569">Which organisational level felt hardest in the scenarios — 
      systemic, team, leader–subordinate, mindset, or technology? What does that suggest about where the boundary work is?</span>
    </div>
    <div style="background:#EFF6FF;border-left:4px solid #2563EB;border-radius:10px;padding:1rem 1.2rem">
      <strong>The scenario that landed</strong><br>
      <span style="font-size:0.9rem;color:#475569">Which scenario felt most uncomfortably familiar?
      What tension in that scenario do we keep managing around rather than attending to?</span>
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
      <p>20 workplace scenarios across five organisational levels — 
      surface where your boundary-crossing capacity is strongest, 
      and where you tend to manage around tensions rather than attend to them.</p>
    </div>""", unsafe_allow_html=True)

    with st.expander("ℹ️ About this tool", expanded=False):
        st.markdown("""
Rather than rating abstract statements about yourself, this diagnostic puts you in 
**20 real workplace situations** — messy, pulled-in-multiple-directions moments 
where the easy path is to keep moving and the harder path is to attend to what's 
actually happening at the boundary.

**Four dimensions** are assessed across **five organisational levels**:

| | Dimension | What it surfaces |
|---|---|---|
| 🔍 | **Boundary Awareness** | Do you notice and name the tensions, or manage around them? |
| 🤝 | **Coordination** | Do you build structures that last, or workarounds that depend on you? |
| 🪞 | **Reflective Capacity** | Do you use difficulty as learning material, or explain it away? |
| ✨ | **Transformative Practice** | Do you generate new practice, or iterate within existing frames? |

**Five organisational levels:** Systemic · Team · Leader–Subordinate · Individual Mindset · Technology

Choose what you would **most likely do** — not the most impressive answer. 
The diagnostic is most useful when it's honest.

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
            # Shuffle option display order per scenario (keeps scoring correct)
            opt_orders = {}
            for sc in SCENARIOS:
                idx_list = list(range(len(sc["options"])))
                random.shuffle(idx_list)
                opt_orders[sc["id"]] = idx_list
            st.session_state.order      = order
            st.session_state.opt_orders = opt_orders
            st.session_state.answers    = {}
            st.session_state.q_idx      = 0
            st.session_state.page       = "quiz"
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# QUIZ
# ─────────────────────────────────────────────────────────────────────────────
def show_quiz():
    idx   = st.session_state.q_idx
    total = len(SCENARIOS)
    sc    = SCENARIOS[st.session_state.order[idx]]
    dim   = DIMENSIONS[sc["dim"]]
    level = LEVEL_LABELS[sc["level"]]

    pct = idx / total
    st.markdown(f"""
    <div class="prog-wrap">
      <div class="prog-label">
        <span>Scenario {idx+1} of {total}</span>
        <span style="color:{dim['color']};font-weight:600">{dim['icon']} {dim['name']}</span>
      </div>
      <div class="prog-bg"><div class="prog-fill" style="width:{pct*100:.0f}%"></div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
      <div class="sc-level">{level}</div>
      <div class="sc-title">{sc['title']}</div>
      <p class="sc-context">{sc['context']}</p>
      <p class="sc-prompt">{sc['prompt']}</p>
    </div>""", unsafe_allow_html=True)

    # Shuffled option display
    opt_order   = st.session_state.opt_orders.get(sc["id"], list(range(len(sc["options"]))))
    display_opts = [sc["options"][i][0] for i in opt_order]
    display_scrs = [sc["options"][i][1] for i in opt_order]

    prev_score  = st.session_state.answers.get(sc["id"])
    default_idx = display_scrs.index(prev_score) if prev_score in display_scrs else 0

    choice = st.radio("", display_opts, index=default_idx, key=f"q_{sc['id']}")
    chosen_score = display_scrs[display_opts.index(choice)]

    is_last = idx == total - 1
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", disabled=(idx == 0)):
            st.session_state.answers[sc["id"]] = chosen_score
            st.session_state.q_idx -= 1
            st.rerun()
    with col2:
        if st.button("See My Results →" if is_last else "Next →"):
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
        st.plotly_chart(make_radar([scores],[name]), use_container_width=True)
    with col2:
        st.plotly_chart(make_bar(scores), use_container_width=True)

    # Level breakdown per dimension
    level_scores = {}
    for sc in SCENARIOS:
        level_scores[(sc["dim"], sc["level"])] = st.session_state.answers.get(sc["id"], 0)

    st.markdown("<h3 style='font-family:Lora,Georgia,serif;color:#1E293B;margin-bottom:0.75rem'>"
                "Dimension Profiles</h3>", unsafe_allow_html=True)

    for key, dim in DIMENSIONS.items():
        s               = scores[key]
        label, lc, tidx = score_tier(s)
        pct             = (s/20)*100

        dim_levels = [(lv, level_scores.get((key, lv), 0)) for lv in LEVEL_LABELS]
        sorted_lvls = sorted(dim_levels, key=lambda x: x[1], reverse=True)
        pill_html = "<div class='level-pills'>"
        for i, (lv, lv_score) in enumerate(sorted_lvls):
            cls = "pill best" if i == 0 else ("pill low" if i == len(sorted_lvls)-1 else "pill")
            pill_html += f"<span class='{cls}'>{LEVEL_LABELS[lv]} {lv_score}/4</span>"
        pill_html += "</div>"

        st.markdown(f"""
        <div class="r-card" style="border-left:5px solid {dim['color']}">
          <div class="r-header">
            <div><div class="r-name">{dim['icon']} {dim['name']}</div>
                 <div class="r-tagline">{dim['tagline']}</div></div>
            <span class="r-badge" style="background:{lc}">{label.upper()}</span>
          </div>
          <div class="r-score">{s}<span> / 20</span></div>
          <div class="r-bar-bg"><div class="r-bar-fill" style="background:{dim['color']};width:{pct:.0f}%"></div></div>
          {pill_html}
          <p class="r-text">{dim['feedback'][tidx]}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="reflect-box">
      <div class="reflect-title">💭 Reflection Prompt</div>
      <p class="reflect-text">
        Which scenario felt most uncomfortably familiar — not because it was hard,
        but because you recognised the impulse to move past it quickly?
        Looking at your level pills: where is the gap largest between your best and lowest 
        organisational level within the same dimension?
        What is one tension you have been managing around that this diagnostic is naming for you?
      </p>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    report = html_report(name, scores, st.session_state.class_code)
    st.download_button("📄 Download My Report (open → Print → Save as PDF)",
                       data=report,
                       file_name=f"BC_Diagnostic_{name.replace(' ','_')}.html",
                       mime="text/html", use_container_width=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    if not st.session_state.submitted:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:#1E293B;margin-bottom:0.4rem">📤 Submit to Class & Research Dataset</div>
          <p style="margin:0;font-size:0.87rem;color:#475569;line-height:1.65">
            Share your dimension scores with the facilitator's live dashboard and the research dataset.
            Only your name and four dimension scores are submitted —
            your individual scenario responses remain private.
          </p>
        </div>""", unsafe_allow_html=True)
        if st.button("✅ Submit to Class"):
            store = get_class_store()
            row   = {
                "timestamp":      datetime.now().strftime("%Y-%m-%d %H:%M"),
                "name":           name,
                "class_code":     st.session_state.class_code,
                "awareness":      scores["awareness"],
                "coordination":   scores["coordination"],
                "reflection":     scores["reflection"],
                "transformation": scores["transformation"],
            }
            store.append({"name": name, "class_code": st.session_state.class_code,
                          "scores": scores, "timestamp": datetime.now().strftime("%H:%M")})
            ok = submit_to_sheets(row)
            st.session_state.submitted = True
            st.session_state.sheets_ok = ok
            st.rerun()
    else:
        ok    = st.session_state.get("sheets_ok", False)
        extra = "and saved to the research dataset ✓" if ok else "(configure Google Sheets to save to research dataset)"
        st.markdown(f"""
        <div class="confirm-box">
          <h3>✅ Submitted to Class Dashboard</h3>
          <p>{extra}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
    if st.button("🔄 Retake Diagnostic"):
        for k in ["page","q_idx","order","opt_orders","answers","submitted","sheets_ok"]:
            st.session_state.pop(k, None)
        st.rerun()

    st.markdown("<p style='text-align:center;color:#CBD5E1;font-size:0.78rem;margin-top:1rem'>"
                "Inspired by Akkerman &amp; Bakker (2011) boundary-crossing theory.</p>",
                unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    apply_css()
    init_state()
    facilitator_sidebar()
    if   st.session_state.fac_mode:         show_facilitator()
    elif st.session_state.page == "welcome": show_welcome()
    elif st.session_state.page == "quiz":    show_quiz()
    elif st.session_state.page == "results": show_results()

if __name__ == "__main__":
    main()
