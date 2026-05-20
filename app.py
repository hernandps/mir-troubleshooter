import streamlit as st
from pathlib import Path
from flows.robot_wont_move import FLOW as FLOW_WONT_MOVE

st.set_page_config(
    page_title="MiR Troubleshooter",
    page_icon="🤖",
    layout="centered",
)


def _stub(title, note):
    return {
        "title": title,
        "start": "stub",
        "nodes": {
            "stub": {
                "type": "solution",
                "severity": "medium",
                "title": f"{title} — Flow Coming Soon",
                "image": None,
                "video": None,
                "steps": [
                    note,
                    "This troubleshooting flow is currently under development.",
                    "In the meantime, contact technical support.",
                    "Have ready: robot serial number + description of when the issue occurs.",
                ],
            }
        },
    }


# Each entry: the flow dict to use + the node to start at.
# "Robot Cannot Move" and "Robot Won't Turn On" share the same flow
# but enter at different nodes, skipping the redundant "Is the robot ON?" question.
FLOWS = {
    "robot_cannot_move": {
        "title": "Robot Cannot Move",
        "flow": FLOW_WONT_MOVE,
        "start": "q_web_interface",
    },
    "robot_wont_turn_on": {
        "title": "Robot Won't Turn On",
        "flow": FLOW_WONT_MOVE,
        "start": "q_unused_days",
    },
    "losing_localization": {
        "title": "Robot Losing Localization",
        "flow": _stub(
            "Robot Losing Localization",
            "Robot is drifting, teleporting on the map, or reporting 'Localization lost'.",
        ),
        "start": "stub",
    },
    "protective_state": {
        "title": "Constantly in Protective State",
        "flow": _stub(
            "Constantly in Protective State",
            "Robot keeps entering protective stop — E-stop or laser fields triggering unexpectedly.",
        ),
        "start": "stub",
    },
    "wifi_problems": {
        "title": "Wi-Fi / Connectivity",
        "flow": _stub(
            "Wi-Fi / Connectivity",
            "Robot drops connection, intermittent network issues, or can't reach the Fleet.",
        ),
        "start": "stub",
    },
    "fleet_problems": {
        "title": "Fleet Manager Problems",
        "flow": _stub(
            "Fleet Manager Problems",
            "Issues with MiR Fleet dispatching, scheduling, or robot not accepting missions.",
        ),
        "start": "stub",
    },
    "mission_problems": {
        "title": "Mission / Application Problems",
        "flow": _stub(
            "Mission / Application Problems",
            "Robot moves but misses positions, overshoots, takes wrong paths, or missions don't complete.",
        ),
        "start": "stub",
    },
    "narrow_spaces": {
        "title": "Won't Go Through Narrow Spaces",
        "flow": _stub(
            "Won't Go Through Narrow Spaces",
            "Robot avoids corridors or doorways it should fit through.",
        ),
        "start": "stub",
    },
}

PROBLEM_CARDS = [
    {
        "key": "robot_cannot_move",
        "icon": "🛑",
        "title": "Robot Cannot Move",
        "desc": "Robot is ON but won't drive — manual or automatic",
        "badge": "Most Common",
    },
    {
        "key": "robot_wont_turn_on",
        "icon": "⚡",
        "title": "Robot Won't Turn On",
        "desc": "No lights or display response when pressing power",
    },
    {
        "key": "losing_localization",
        "icon": "📍",
        "title": "Losing Localization",
        "desc": "Robot doesn't know where it is, drifts on the map",
    },
    {
        "key": "protective_state",
        "icon": "🛡️",
        "title": "Constantly in Protective State",
        "desc": "Robot keeps stopping — E-stop or laser fields triggering",
    },
    {
        "key": "wifi_problems",
        "icon": "📶",
        "title": "Wi-Fi / Connectivity",
        "desc": "Connection drops, can't reach the robot or Fleet",
    },
    {
        "key": "fleet_problems",
        "icon": "🗄️",
        "title": "Fleet Manager Problems",
        "desc": "Dispatching, scheduling, or mission assignment issues",
    },
    {
        "key": "mission_problems",
        "icon": "⚙️",
        "title": "Mission / Application Problems",
        "desc": "Robot moves but misses positions or missions don't complete",
    },
    {
        "key": "narrow_spaces",
        "icon": "🚪",
        "title": "Won't Go Through Narrow Spaces",
        "desc": "Robot avoids corridors or doorways it should fit through",
    },
]

SEVERITY_BADGE = {
    "easy":   ("green",  "Easy Fix"),
    "medium": ("orange", "Moderate"),
    "hard":   ("red",    "Escalate"),
}

# Inject CSS: make Streamlit's "primary" button green instead of blue.
# Good/expected answers use type="primary" → green.
# Warn/problem answers use type="secondary" → default gray + ⚠️ prefix in label.
st.markdown("""
<style>
/* Cover old (baseButton-primary) and new (stBaseButton-primary) Streamlit versions */
button[data-testid="stBaseButton-primary"],
button[data-testid="baseButton-primary"],
button[kind="primary"] {
    background-color: #2E7D4F !important;
    border-color: #2E7D4F !important;
    color: white !important;
}
button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="baseButton-primary"]:hover,
button[kind="primary"]:hover {
    background-color: #1B5E35 !important;
    border-color: #1B5E35 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


def reset():
    st.session_state.current_node = None
    st.session_state.history = []
    st.session_state.selected_flow = None


def go_back():
    if st.session_state.history:
        st.session_state.current_node = st.session_state.history.pop()
    else:
        reset()


def render_nav_buttons(node_id):
    st.write("")
    st.divider()
    col_back, _, col_restart = st.columns([3, 5, 2])
    with col_back:
        if st.button("← Go back", key=f"{node_id}_nav_back", use_container_width=True):
            go_back()
            st.rerun()
    with col_restart:
        if st.button("Start over", key=f"{node_id}_nav_restart"):
            reset()
            st.rerun()


def render_image(path_str):
    if not path_str:
        return
    paths = [path_str] if isinstance(path_str, str) else path_str
    for p_str in paths:
        p = Path(p_str)
        if p.exists():
            st.image(str(p), use_container_width=True)
        else:
            st.info(f"📷 Image will appear here: `{p_str}`")


def render_video(path_str):
    if not path_str:
        return
    p = Path(path_str)
    if p.exists():
        st.video(str(p))
    else:
        st.info(f"🎥 Video will appear here: `{path_str}`")


def render_question(node_id, node):
    st.subheader(node["text"])
    if node.get("hint"):
        st.caption(f"Tip: {node['hint']}")
    if node.get("info"):
        st.info(node["info"])

    render_image(node.get("image"))
    render_video(node.get("video"))
    st.write("")

    cols = st.columns(len(node["options"]))
    for i, option in enumerate(node["options"]):
        with cols[i]:
            style = option.get("style", "neutral")
            label = option["label"]
            if style == "warn":
                label = f"⚠️ {label}"
            btn_type = "primary" if style == "good" else "secondary"
            if st.button(label, key=f"{node_id}_{i}", use_container_width=True, type=btn_type):
                st.session_state.history.append(node_id)
                st.session_state.current_node = option["next"]
                st.rerun()

    render_nav_buttons(node_id)


def render_checklist(node_id, node):
    st.subheader(node["text"])
    if node.get("hint"):
        st.caption(f"Tip: {node['hint']}")
    if node.get("info"):
        st.info(node["info"])

    render_image(node.get("image"))
    render_video(node.get("video"))
    st.write("")

    st.write("**Confirm each step before continuing:**")
    checked = {}
    for item in node["items"]:
        checked[item["key"]] = st.checkbox(
            item["label"],
            key=f"{node_id}_chk_{item['key']}",
        )

    st.write("")
    cols = st.columns(len(node["options"]))
    for i, option in enumerate(node["options"]):
        with cols[i]:
            style = option.get("style", "neutral")
            label = option["label"]
            if style == "warn":
                label = f"⚠️ {label}"
            btn_type = "primary" if style == "good" else "secondary"
            required = option.get("requires", [])
            disabled = any(not checked.get(k, False) for k in required)
            if st.button(
                label,
                key=f"{node_id}_{i}",
                use_container_width=True,
                type=btn_type,
                disabled=disabled,
            ):
                st.session_state.history.append(node_id)
                st.session_state.current_node = option["next"]
                st.rerun()

    # Show hint when the green button is still locked
    required_opts = [o for o in node["options"] if o.get("requires")]
    if required_opts:
        remaining = [k for k in required_opts[0]["requires"] if not checked.get(k, False)]
        if remaining:
            st.caption(f"Complete {len(remaining)} more step(s) above to enable the green button.")

    render_nav_buttons(node_id)


def render_solution(node):
    color, label = SEVERITY_BADGE.get(node.get("severity", "medium"), ("orange", "Moderate"))
    st.markdown(f"### {node['title']}")
    st.markdown(f":{color}[**{label}**]")
    st.divider()

    render_image(node.get("image"))
    render_video(node.get("video"))

    st.write("**Steps to resolve:**")
    for i, step in enumerate(node["steps"], 1):
        st.markdown(f"{i}. {step}")

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Problem solved — Start over", use_container_width=True):
            reset()
            st.rerun()
    with col2:
        if st.button("This didn't help — Go back", use_container_width=True):
            go_back()
            st.rerun()


def render_breadcrumbs(title):
    if not st.session_state.history:
        return
    steps = len(st.session_state.history)
    st.caption(f"Step {steps + 1}  •  {title}")


# --- Init session state ---
if "current_node" not in st.session_state:
    st.session_state.current_node = None
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_flow" not in st.session_state:
    st.session_state.selected_flow = None

# --- Header ---
st.title("🤖 MiR Robot Troubleshooter")
st.divider()

# --- Home screen ---
if st.session_state.selected_flow is None:
    st.subheader("What is the problem?")
    st.caption("Select the issue that best describes what you are seeing.")
    st.write("")

    for i in range(0, len(PROBLEM_CARDS), 2):
        cols = st.columns(2, gap="medium")
        for j, col in enumerate(cols):
            idx = i + j
            if idx >= len(PROBLEM_CARDS):
                break
            card = PROBLEM_CARDS[idx]
            with col:
                with st.container(border=True):
                    st.markdown(f"## {card['icon']}")
                    badge = f"  `{card['badge']}`" if card.get("badge") else ""
                    st.markdown(f"**{card['title']}**{badge}")
                    st.caption(card["desc"])
                    st.write("")
                    if st.button(
                        "Start troubleshooting →",
                        key=f"card_{card['key']}",
                        use_container_width=True,
                    ):
                        entry = FLOWS[card["key"]]
                        st.session_state.selected_flow = card["key"]
                        st.session_state.current_node = entry["start"]
                        st.session_state.history = []
                        st.rerun()

# --- Troubleshooting flow ---
else:
    entry = FLOWS[st.session_state.selected_flow]
    flow = entry["flow"]
    render_breadcrumbs(entry["title"])

    node_id = st.session_state.current_node
    node = flow["nodes"][node_id]

    if node["type"] == "question":
        render_question(node_id, node)
    elif node["type"] == "checklist":
        render_checklist(node_id, node)
    elif node["type"] == "solution":
        render_solution(node)
