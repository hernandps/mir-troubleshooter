import streamlit as st
import json
import time
import random
from pathlib import Path
from flows.robot_wont_move import FLOW as FLOW_WONT_MOVE
from flows.protective_state import FLOW as FLOW_PROTECTIVE
from flows.wifi_connectivity import FLOW as FLOW_WIFI
from flows.losing_localization import FLOW as FLOW_LOCALIZATION
from flows.not_starting import FLOW as FLOW_NOT_STARTING
from flows.battery import FLOW as FLOW_BATTERY
from flows.docking import FLOW as FLOW_DOCKING
from flows.charging_station import FLOW as FLOW_CHARGING
from flows.camera_3d import FLOW as FLOW_CAMERA
from flows.can_bus import FLOW as FLOW_CAN_BUS

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


# ── CONTRIBUTION SYSTEM ───────────────────────────────────────────────────────
# Users can upload real photos/videos and report corrections.
# All submissions are saved to contributions/ for the operator to review.

_CONTRIB = Path("contributions")


def _load_feedback():
    fb_file = _CONTRIB / "feedback.json"
    if fb_file.exists():
        try:
            with open(fb_file, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_feedback(flow_key, node_id, node_label, message):
    _CONTRIB.mkdir(exist_ok=True)
    entries = _load_feedback()
    entries.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "flow": flow_key,
        "node": node_id,
        "step": node_label,
        "message": message,
    })
    with open(_CONTRIB / "feedback.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def _save_upload(flow_key, node_id, uploaded_file):
    upload_dir = _CONTRIB / "uploads" / flow_key / node_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    safe_name = uploaded_file.name.replace(" ", "_")
    filename = f"{ts}_{safe_name}"
    with open(upload_dir / filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    with open(upload_dir / f"{ts}_meta.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "flow": flow_key,
            "node": node_id,
            "original_name": uploaded_file.name,
            "saved_as": filename,
        }, f, indent=2)


def _count_uploads():
    up_dir = _CONTRIB / "uploads"
    if not up_dir.exists():
        return 0
    return sum(1 for f in up_dir.rglob("*") if f.is_file() and not f.name.endswith("_meta.json"))


def _check_admin_password(entered: str) -> bool:
    try:
        correct = st.secrets.get("admin_password", "mir-admin")
    except Exception:
        correct = "mir-admin"
    return entered.strip() == correct


# ── COMMENTS ──────────────────────────────────────────────────────────────────

def _load_comments():
    cf = _CONTRIB / "comments.json"
    if cf.exists():
        try:
            with open(cf, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_comment(flow_key, node_id, message, author):
    _CONTRIB.mkdir(exist_ok=True)
    entries = _load_comments()
    comment_id = f"{time.strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
    entries.append({
        "id": comment_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "flow": flow_key,
        "node": node_id,
        "message": message,
        "author": author.strip() or None,
    })
    with open(_CONTRIB / "comments.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def _delete_comment(comment_id):
    entries = [c for c in _load_comments() if c.get("id") != comment_id]
    with open(_CONTRIB / "comments.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def render_comments_widget(node_label):
    node_id  = st.session_state.get("current_node", "unknown")
    flow_key = st.session_state.get("selected_flow", "home")
    wkey     = f"{flow_key}__{node_id}"

    all_comments  = _load_comments()
    node_comments = [c for c in all_comments if c["flow"] == flow_key and c["node"] == node_id]

    # ── Show existing comments ─────────────────────────────────────────────
    if node_comments:
        st.write("")
        st.caption("**💬 Comments:**")
        for c in node_comments:
            author_part = f" — *{c['author']}*" if c.get("author") else ""
            date_part   = c["timestamp"].split(" ")[0]
            bubble = (
                f"<div style='"
                f"background:#f0f2f6;padding:8px 14px;border-radius:8px;margin:4px 0;"
                f"border-left:3px solid #ccc;'>"
                f"{c['message']}{author_part} "
                f"<span style='color:#aaa;font-size:0.8em;'>· {date_part}</span>"
                f"</div>"
            )
            if st.session_state.admin_mode:
                col_msg, col_del = st.columns([11, 1])
                with col_msg:
                    st.markdown(bubble, unsafe_allow_html=True)
                with col_del:
                    if st.button("🗑️", key=f"del_{c['id']}", help="Delete comment"):
                        _delete_comment(c["id"])
                        st.rerun()
            else:
                st.markdown(bubble, unsafe_allow_html=True)

    # ── Add a comment ──────────────────────────────────────────────────────
    with st.expander("💬 Add a comment"):
        st.caption(
            "Share a tip, a gotcha, or anything extra that helped you. "
            "Your comment will be visible to everyone."
        )
        msg = st.text_area(
            "Comment",
            placeholder="e.g. 'On the MiR600 this button is on the right side, not the left'",
            key=f"cmsg_{wkey}",
            label_visibility="collapsed",
        )
        name = st.text_input(
            "Name",
            placeholder="Your name (optional)",
            key=f"cname_{wkey}",
            label_visibility="collapsed",
        )
        if st.button("Post comment", key=f"cpost_{wkey}", use_container_width=True):
            if msg.strip():
                _save_comment(flow_key, node_id, msg.strip(), name)
                st.success("Comment posted!")
                st.rerun()
            else:
                st.warning("Please write something first.")


def render_contribute_widget(node_label):
    node_id = st.session_state.get("current_node", "unknown")
    flow_key = st.session_state.get("selected_flow", "home")
    widget_key = f"{flow_key}__{node_id}"

    st.write("")
    with st.expander("📸 Add a photo  ·  ⚠️ Report an issue"):
        tab_up, tab_fb = st.tabs(["📁 Upload photo / video", "⚠️ Report an issue"])

        with tab_up:
            st.caption(
                "Have a real photo or video that shows this step? Upload it here — "
                "it helps people who struggle with text-only instructions."
            )
            uploaded = st.file_uploader(
                "file",
                type=["jpg", "jpeg", "png", "gif", "mp4", "mov", "webp"],
                key=f"up_{widget_key}",
                label_visibility="collapsed",
            )
            if uploaded:
                if uploaded.type.startswith("image"):
                    st.image(uploaded, use_container_width=True)
                if st.button(
                    "Submit photo / video",
                    key=f"sub_up_{widget_key}",
                    use_container_width=True,
                ):
                    _save_upload(flow_key, node_id, uploaded)
                    st.success("Thank you! Your file has been saved for review.")

        with tab_fb:
            st.caption(
                "Found a mistake, a wrong image, or a missing step? "
                "Describe it below and we will fix it."
            )
            msg = st.text_area(
                "msg",
                placeholder=(
                    "e.g. 'The relay image is for MiR250 but I have a MiR600'\n"
                    "      'Step 3 is missing — you also need to press the Reset button first'"
                ),
                key=f"fb_{widget_key}",
                label_visibility="collapsed",
            )
            if st.button("Send feedback", key=f"sub_fb_{widget_key}", use_container_width=True):
                if msg.strip():
                    _save_feedback(flow_key, node_id, node_label, msg)
                    st.success("Feedback saved. Thank you!")
                else:
                    st.warning("Please write something before submitting.")


# ── FLOWS ─────────────────────────────────────────────────────────────────────
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
    "not_starting": {
        "title": "Robot Not Starting Up",
        "flow": FLOW_NOT_STARTING,
        "start": "q_power_button_color",
    },
    "battery_issues": {
        "title": "Battery Issues",
        "flow": FLOW_BATTERY,
        "start": "q_battery_symptom",
    },
    "losing_localization": {
        "title": "Robot Losing Localization",
        "flow": FLOW_LOCALIZATION,
        "start": "q_localization_symptom",
    },
    "protective_state": {
        "title": "Constantly in Protective State",
        "flow": FLOW_PROTECTIVE,
        "start": "q_stop_type",
    },
    "wifi_problems": {
        "title": "Wi-Fi / Connectivity",
        "flow": FLOW_WIFI,
        "start": "q_connection_method",
    },
    "docking_problems": {
        "title": "Docking Issues",
        "flow": FLOW_DOCKING,
        "start": "q_multiple_robots",
    },
    "charging_station": {
        "title": "Charging Station Not Charging",
        "flow": FLOW_CHARGING,
        "start": "q_charge_symptom",
    },
    "camera_3d": {
        "title": "3D Camera Issues",
        "flow": FLOW_CAMERA,
        "start": "q_camera_symptom",
    },
    "can_bus": {
        "title": "CAN Bus / Lights Not Working",
        "flow": FLOW_CAN_BUS,
        "start": "q_can_symptoms",
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
        "key": "protective_state",
        "icon": "🛡️",
        "title": "Constantly in Protective State",
        "desc": "Robot keeps stopping — E-stop or laser fields triggering",
    },
    {
        "key": "not_starting",
        "icon": "🔌",
        "title": "Robot Not Starting Up",
        "desc": "Power button on, but status lights stuck yellow or no startup",
    },
    {
        "key": "robot_wont_turn_on",
        "icon": "⚡",
        "title": "Robot Won't Turn On",
        "desc": "No lights or display response when pressing power",
    },
    {
        "key": "battery_issues",
        "icon": "🔋",
        "title": "Battery Issues",
        "desc": "Battery won't charge, deep sleep, power save mode",
    },
    {
        "key": "wifi_problems",
        "icon": "📶",
        "title": "Wi-Fi / Connectivity",
        "desc": "Connection drops, can't reach the robot or Fleet",
    },
    {
        "key": "docking_problems",
        "icon": "🎯",
        "title": "Docking Issues",
        "desc": "Robot fails to dock to markers, charging stations, or racks",
    },
    {
        "key": "charging_station",
        "icon": "⚡",
        "title": "Charging Station Not Charging",
        "desc": "Robot docks but doesn't charge, or charging stops early",
    },
    {
        "key": "losing_localization",
        "icon": "📍",
        "title": "Losing Localization",
        "desc": "Robot doesn't know where it is, drifts on the map",
    },
    {
        "key": "camera_3d",
        "icon": "📷",
        "title": "3D Camera Issues",
        "desc": "Phantom obstacles, camera errors, detection failures",
    },
    {
        "key": "can_bus",
        "icon": "💡",
        "title": "CAN Bus / Lights Not Working",
        "desc": "Indicator lights faulty, proximity sensors not responding",
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
    render_comments_widget(node["text"])
    render_contribute_widget(node["text"])


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
    render_comments_widget(node["text"])
    render_contribute_widget(node["text"])


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

    render_comments_widget(node["title"])
    render_contribute_widget(node["title"])


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
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

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

    # --- Admin panel (password-protected) ---
    st.write("")
    st.divider()

    if st.session_state.admin_mode:
        # ── Logged-in view ────────────────────────────────────────────────────
        fb_entries = _load_feedback()
        n_uploads = _count_uploads()
        col_title, col_logout = st.columns([5, 1])
        with col_title:
            st.markdown(f"**Admin — {len(fb_entries)} feedback · {n_uploads} upload(s)**")
        with col_logout:
            if st.button("Log out", key="admin_logout"):
                st.session_state.admin_mode = False
                st.rerun()

        if not fb_entries and not n_uploads:
            st.caption("No contributions yet.")
        else:
            if n_uploads:
                up_dir = _CONTRIB / "uploads"
                st.write(f"**Uploaded files** (saved in `contributions/uploads/`)")
                for meta_file in sorted(up_dir.rglob("*_meta.json"), reverse=True)[:10]:
                    try:
                        with open(meta_file, encoding="utf-8") as mf:
                            meta = json.load(mf)
                        media_path = meta_file.parent / meta["saved_as"]
                        col_a, col_b = st.columns([2, 3])
                        with col_a:
                            st.caption(
                                f"**{meta['timestamp']}**  \n"
                                f"Flow: `{meta['flow']}`  \n"
                                f"Node: `{meta['node']}`  \n"
                                f"File: `{meta['original_name']}`"
                            )
                        with col_b:
                            if media_path.exists():
                                suffix = media_path.suffix.lower()
                                if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
                                    st.image(str(media_path), use_container_width=True)
                                elif suffix in {".mp4", ".mov"}:
                                    st.video(str(media_path))
                    except Exception:
                        pass

            if fb_entries:
                st.write(f"**Feedback reports:**")
                for entry in reversed(fb_entries[-20:]):
                    st.markdown(
                        f"**{entry['timestamp']}** · Flow: `{entry['flow']}` · "
                        f"Step: _{entry.get('step', entry['node'])}_"
                    )
                    st.info(entry["message"])

    else:
        # ── Login view (inconspicuous) ─────────────────────────────────────────
        with st.expander("Admin"):
            pwd = st.text_input(
                "Password",
                type="password",
                key="admin_pwd_input",
                label_visibility="collapsed",
                placeholder="Admin password",
            )
            if st.button("Log in", key="admin_login_btn"):
                if _check_admin_password(pwd):
                    st.session_state.admin_mode = True
                    st.rerun()
                else:
                    st.error("Wrong password.")

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
