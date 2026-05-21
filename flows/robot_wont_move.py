FLOW = {
    "title": "Robot Won't Move",
    "start": "q_robot_on",
    "nodes": {

        # ── PHASE 1: POWER ────────────────────────────────────────────────

        "q_robot_on": {
            "type": "question",
            "text": "Is the robot ON?",
            "hint": "Check if the lights are on and the top display is active.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — robot is on",        "next": "q_web_interface", "style": "good"},
                {"label": "No — robot won't turn on", "next": "q_unused_days",   "style": "warn"},
            ],
        },

        "q_unused_days": {
            "type": "question",
            "text": "Has the robot been unused for many days or weeks?",
            "hint": "Batteries that sit unused for a long time can enter deep sleep mode.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — sitting unused for a while", "next": "sol_deep_sleep",        "style": "neutral"},
                {"label": "No — it was in use recently",      "next": "sol_battery_discharged", "style": "neutral"},
            ],
        },

        # ── PHASE 2: WEB INTERFACE ────────────────────────────────────────

        "q_web_interface": {
            "type": "question",
            "text": "Can you access the robot's web interface?",
            "hint": "Wait ~5 minutes after turning on. ⚠️ Robot lights only confirm the power board is on — they say nothing about the CPU.",
            "image": None,
            "video": None,
            "info": (
                "How to connect:\n"
                "• Service port (Ethernet to laptop) → IP: 192.168.12.20  ← always works\n"
                "• Old robot WiFi (MiR-[serial]) → IP: 192.168.12.20\n"
                "• Client WiFi → use the IP assigned by the router (must know it beforehand)\n"
                "If you don't know the client WiFi IP → use the service port."
            ),
            "options": [
                {"label": "Yes — I can see the interface", "next": "q_reset_button", "style": "good"},
                {"label": "No — I can't reach it",         "next": "q_ping",         "style": "warn"},
            ],
        },

        "q_ping": {
            "type": "question",
            "text": "Try pinging the robot. Do you get a response?",
            "hint": "Open Command Prompt and run: ping 192.168.12.20 (service port or old robot WiFi) or your assigned IP (client WiFi).",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — ping responds",   "next": "sol_cpu_software",   "style": "good"},
                {"label": "No — no ping response", "next": "sol_connection_issue", "style": "warn"},
            ],
        },

        # ── PHASE 3: RESET BUTTON ─────────────────────────────────────────

        "q_reset_button": {
            "type": "question",
            "text": "Is the robot asking you to press the Reset button?",
            "hint": "The blue button on the robot should be flashing when ready to reset.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — blue button is flashing", "next": "q_after_reset",  "style": "good"},
                {"label": "No — red lights, no prompt",    "next": "q_key_selector", "style": "warn"},
            ],
        },

        "q_after_reset": {
            "type": "question",
            "text": "Press the blue Reset button, then press Play in the web interface. Do the lights turn GREEN and the robot move normally?",
            "hint": "After Reset: lights turn yellow (paused — this is normal). After Play: lights turn green (ready).",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — green lights, robot is working",          "next": "sol_resolved",        "style": "good"},
                {"label": "No — robot is in ready state but still won't move", "next": "q_manual_move", "style": "warn"},
            ],
        },

        "q_key_selector": {
            "type": "question",
            "text": "Is the key selector switch in MANUAL position?",
            "hint": "Check the key switch on the robot. In MANUAL mode the robot will never ask for Reset.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — key is in MANUAL",   "next": "sol_key_to_automatic", "style": "warn"},
                {"label": "No — key is in AUTOMATIC", "next": "q_brake_release",      "style": "good"},
            ],
        },

        "q_brake_release": {
            "type": "question",
            "text": "Can you push the robot with your hands?",
            "hint": "When powered on normally the brakes are engaged — the robot should NOT move when pushed.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — robot moves when pushed", "next": "sol_brake_release", "style": "warn"},
                {"label": "No — robot doesn't move",       "next": "q_plc_status",      "style": "good"},
            ],
        },

        "q_plc_status": {
            "type": "question",
            "text": "In the web interface, go to Monitoring → Hardware Health. What is the Safety PLC status?",
            "hint": "Green = communication OK. Black = no communication with PLC.",
            "image": None,
            "video": None,
            "options": [
                {"label": "PLC is green — communication OK", "next": "sol_cpu_issue",  "style": "good"},
                {"label": "PLC is black — no communication", "next": "sol_plc_issue",  "style": "warn"},
            ],
        },

        # ── PHASE 4: ROBOT IN READY STATE BUT WON'T MOVE ─────────────────

        "q_manual_move": {
            "type": "question",
            "text": "Switch to MANUAL mode and try moving the robot using the joystick. Does it move?",
            "hint": "⚠️ Before testing: confirm no obstacles around the robot, or mute the protective fields if needed.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — moves in manual but not automatic", "next": "sol_autonomous_issue", "style": "neutral"},
                {"label": "No — won't move in manual either",        "next": "q_relay_voltage_check", "style": "warn"},
            ],
        },


        "q_boggy_current": {
            "type": "question",
            "text": "When the robot tries to move, is current present at the boggies but the robot doesn't move at all?",
            "hint": "Expected current when moving: ~15A (MiR250) or ~45A (MiR600). If current is present and stuck but the robot doesn't move, the boggy brake is likely not releasing.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — current present but robot is stuck", "next": "sol_boggy_issue",      "style": "warn"},
                {"label": "No — no current at all",                   "next": "sol_motor_controller", "style": "warn"},
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────

        "sol_resolved": {
            "type": "solution",
            "severity": "easy",
            "title": "Robot Is Working Normally",
            "image": None,
            "video": None,
            "steps": [
                "The robot is now in READY state with green lights.",
                "Resume normal operations.",
            ],
        },

        "sol_deep_sleep": {
            "type": "solution",
            "severity": "easy",
            "title": "Battery in Deep Sleep Mode",
            "image": "assets/images/MiR250 yellow status lights.jpg",
            "video": None,
            "steps": [
                "Locate the battery lever on the side of the robot.",
                "Pull the lever to disconnect the battery and hold for **30 seconds**.",
                "Reconnect the battery by releasing the lever back into position.",
                "Wait **3–4 seconds**.",
                "Try turning the robot on again — it should boot normally.",
            ],
        },

        "sol_battery_discharged": {
            "type": "solution",
            "severity": "medium",
            "title": "Battery Fully Discharged",
            "image": None,
            "video": None,
            "steps": [
                "If you have a spare battery, swap it in and try turning the robot on.",
                "If no spare is available, charge the battery using the **3A charger** (small charger).",
                "Connect the charger directly to the battery and wait until it has enough charge.",
                "Reinstall the battery and try turning the robot on again.",
            ],
        },

        "sol_connection_issue": {
            "type": "solution",
            "severity": "medium",
            "title": "Cannot Reach the Robot — Connection Problem",
            "image": None,
            "video": None,
            "steps": [
                "Confirm you are connected to the correct network.",
                "**Service port (Ethernet):** Connect cable from robot service port directly to your laptop → IP **192.168.12.20**.",
                "**Old robot WiFi:** Connect to `MiR-[serial number]` access point → IP **192.168.12.20**.",
                "**Client WiFi:** You must already know the IP assigned by the router. If unknown, use the service port instead.",
                "Try pinging again after reconnecting.",
            ],
        },

        "sol_cpu_software": {
            "type": "solution",
            "severity": "hard",
            "title": "CPU Reachable but Web Interface Not Loading",
            "image": None,
            "video": None,
            "steps": [
                "The CPU is on (ping responds) but the software is not running correctly.",
                "Possible causes: ROS crashed, database corrupted, or other software fault.",
                "Try a full restart from the power button.",
                "If the issue persists after restart, direct Linux access (SSH) may be needed.",
                "Contact technical support with the robot serial number and a description of the problem.",
            ],
        },

        "sol_key_to_automatic": {
            "type": "solution",
            "severity": "easy",
            "title": "Key Selector Is in MANUAL",
            "image": None,
            "video": None,
            "steps": [
                "Turn the key selector to the **AUTOMATIC** position.",
                "Wait a few seconds — the robot should now ask you to press the Reset button.",
                "Press the blue Reset button → yellow lights → press Play → green lights = ready. ✓",
                "Note: if the robot still doesn't ask for Reset after switching to Automatic, there may be another hardware error. Check Hardware Health in the web interface.",
            ],
        },

        "sol_brake_release": {
            "type": "solution",
            "severity": "easy",
            "title": "Manual Brake Release Switch Is ON",
            "image": None,
            "video": None,
            "steps": [
                "Locate the Manual Brake Release **switch** on the back of the robot (it is a two-way switch, not a button).",
                "Flip the switch to the **OFF** position.",
                "Confirm the key selector is in **AUTOMATIC**.",
                "Open the web interface and tap the **bell icon** (notifications).",
                "Find and clear the **Sanity Check Error**.",
                "The blue Reset button should now flash → press it.",
                "Yellow lights → press Play → green lights = ready. ✓",
            ],
        },

        "sol_plc_issue": {
            "type": "solution",
            "severity": "hard",
            "title": "Safety PLC — No Communication",
            "image": None,
            "video": None,
            "steps": [
                "Open web interface → **Monitoring → Hardware Health** → check PLC status.",
                "Black = no communication. Green = OK.",
                "To confirm: open Command Prompt and run `ping 192.168.12.9`.",
                "⚠️ This only works when connected via **service port** or **robot's own WiFi** — not client WiFi.",
                "If no ping response → PLC is unreachable. Check PLC power and connections.",
                "Contact technical support if the PLC cannot be reached.",
            ],
        },

        "sol_cpu_issue": {
            "type": "solution",
            "severity": "hard",
            "title": "CPU May Not Be Running",
            "image": [
                "assets/images/robot computer power button MiR250.jpg",
                "assets/images/robot computer power button MiR600.jpg",
            ],
            "video": None,
            "steps": [
                "Try pressing the power button directly on the CPU unit inside the robot.",
                "Confirm whether the CPU powers on.",
                "If CPU is on but web interface is still inaccessible, the SSD may be corrupted.",
                "Contact technical support — field repair options are very limited for CPU issues.",
            ],
        },

        "sol_autonomous_issue": {
            "type": "solution",
            "severity": "medium",
            "title": "Moves in Manual but Not in Automatic",
            "image": None,
            "video": None,
            "steps": [
                "The hardware (power, relays, motor controller, boggies) is working correctly.",
                "The problem is likely in the mission system, map, or navigation software.",
                "Check: Is there a valid map loaded? Is the robot localized on the map?",
                "Check the mission queue — is there an active mission? Is it paused?",
                "Check for any errors in the web interface notification bell.",
                "Contact support if no obvious error is found.",
            ],
        },

        # ── RELAY DIAGNOSTIC SUB-FLOW ─────────────────────────────────────
        # Entry: q_relay_check → here when fault detected

        "q_relay_voltage_check": {
            "type": "checklist",
            "text": "STO Relay Voltage Check — K1 and K2",
            "hint": "Use a multimeter. Measure at the input and output terminals of each relay while the robot is in READY state.",
            "image": [
                "assets/images/Relay K1 mir250.jpeg",
                "assets/images/relay mir600.jpeg",
            ],
            "video": None,
            "info": (
                "Expected voltage when robot is in READY state and trying to move: **47–52 V** at both relay terminals.\n\n"
                "K1 and K2 are wired in series — both must be working for the robot to move."
            ),
            "items": [
                {
                    "key": "ready_state",
                    "label": "Robot is in READY state (green lights). Protective fields are clear or muted so the robot can attempt to move.",
                },
                {
                    "key": "voltage_k1",
                    "label": "K1 relay (right side): measured voltage at terminals — reading is in the range 47–52 V.",
                },
                {
                    "key": "voltage_k2",
                    "label": "K2 relay (left side): measured voltage at terminals — reading is in the range 47–52 V.",
                },
            ],
            "options": [
                {
                    "label": "Both K1 and K2: voltage in range (47–52 V)",
                    "next": "q_relay_feedback_check",
                    "style": "good",
                    "requires": ["ready_state", "voltage_k1", "voltage_k2"],
                },
                {
                    "label": "One or both relays: out of range or no voltage",
                    "next": "q_relay_stuck",
                    "style": "warn",
                },
                {
                    "label": "Relays look fine in Hardware Health — skip this check",
                    "next": "q_boggy_current",
                    "style": "neutral",
                },
            ],
        },

        "q_relay_stuck": {
            "type": "question",
            "text": "Relay voltage out of range — try the manual override button",
            "hint": "Remove the front cap of the relay unit to access the override button. Press it ONCE only.",
            "image": [
                "assets/images/removed front cover.jpeg",
                "assets/images/Relay K1 mir250.jpeg",
                "assets/images/relay mir600.jpeg",
            ],
            "video": None,
            "info": (
                "The relay may be physically stuck — the coil activates but the contact does not switch.\n\n"
                "**How to unstick it:**\n"
                "1. Remove the front cover of the relay unit.\n"
                "2. Locate the small manual override button on the relay body.\n"
                "3. Press it **ONCE** while the robot is in READY state.\n"
                "4. Re-measure the voltage at the relay terminals.\n\n"
                "⚠️ **Warning:** Pressing the override button too many times will trigger a **STO Relay Feedback error** by itself — "
                "the PLC detects unexpected relay activation and locks out. Press once and wait."
            ),
            "options": [
                {
                    "label": "Pressed override once — voltage is now 47–52 V on both relays",
                    "next": "sol_relay_recovered",
                    "style": "good",
                },
                {
                    "label": "Still out of range after pressing the override button",
                    "next": "sol_relay_replace",
                    "style": "warn",
                },
            ],
        },

        "q_relay_feedback_check": {
            "type": "checklist",
            "text": "Relay Feedback Signal Check",
            "hint": "Keep the web interface open on Monitoring → Hardware Health while doing this test.",
            "image": None,
            "video": None,
            "info": (
                "Voltage is correct on both relays, but the robot still won't move.\n\n"
                "Now check if the **PLC is receiving the relay feedback signal**. "
                "When the relay activates, it sends a confirmation signal back to the PLC. "
                "If this signal is missing or too slow, the PLC triggers a **STO Relay Feedback error** and blocks movement.\n\n"
                "**How to test:**\n"
                "Switch robot from Manual → Automatic. Try to move the robot (joystick or mission). "
                "Watch the K1 and K2 relay status indicators in Hardware Health — they should activate when the robot tries to move."
            ),
            "items": [
                {
                    "key": "auto_mode",
                    "label": "Robot is in Automatic mode, READY state (green lights). Web interface open on Hardware Health.",
                },
                {
                    "key": "feedback_k1",
                    "label": "Tried to move the robot — K1 relay indicator activates (turns ON) in Hardware Health.",
                },
                {
                    "key": "feedback_k2",
                    "label": "Tried to move the robot — K2 relay indicator activates (turns ON) in Hardware Health.",
                },
            ],
            "options": [
                {
                    "label": "Both K1 and K2 feedback signals activate when moving",
                    "next": "sol_relay_mech_other",
                    "style": "good",
                    "requires": ["auto_mode", "feedback_k1", "feedback_k2"],
                },
                {
                    "label": "One or both feedback signals do NOT activate",
                    "next": "sol_relay_feedback_err",
                    "style": "warn",
                },
            ],
        },

        "sol_relay_recovered": {
            "type": "solution",
            "severity": "easy",
            "title": "Relay Was Stuck — Now Recovered",
            "image": None,
            "video": None,
            "steps": [
                "The relay was physically stuck. Pressing the manual override button released it.",
                "Voltage is now in the 47–52 V range — the relay is functioning correctly.",
                "Test the robot: switch to Automatic → press Reset → press Play → try to move.",
                "⚠️ If the problem returns repeatedly, the relay contacts are wearing out and the relay should be replaced proactively.",
                "Note which relay failed (K1, K2, or both) for your maintenance records.",
            ],
        },

        "sol_relay_replace": {
            "type": "solution",
            "severity": "hard",
            "title": "Relay Must Be Replaced",
            "image": [
                "assets/images/Relay K1 mir250.jpeg",
                "assets/images/relay mir600.jpeg",
            ],
            "video": None,
            "steps": [
                "Voltage remains out of range even after pressing the manual override — the relay is electrically or mechanically faulty.",
                "Note which relay is failing: K1 (right side), K2 (left side), or both.",
                "The relay must be replaced. Do not continue operating the robot.",
                "Contact your MiR distributor or technical support.",
                "Have ready: robot serial number, which relay failed (K1/K2), and the voltage readings you measured.",
            ],
        },

        "sol_relay_feedback_err": {
            "type": "solution",
            "severity": "hard",
            "title": "STO Relay Feedback Error",
            "image": None,
            "video": None,
            "steps": [
                "The relay voltage is correct (47–52 V) but the PLC is not receiving the feedback confirmation signal fast enough — or not at all.",
                "The PLC activates the relay and waits for a confirmation. If it doesn't arrive in time, it locks out and triggers the STO Relay Feedback error.",
                "Possible causes: worn relay feedback contact, loose wiring at the feedback terminal, or the relay is failing internally.",
                "Check the wiring connections at the feedback terminals of the affected relay (K1 or K2).",
                "If wiring looks intact, the relay's internal feedback contact is likely worn out — the relay must be replaced.",
                "Contact technical support with: serial number, which relay (K1/K2), and confirmation that voltage was in range.",
            ],
        },

        "sol_relay_mech_other": {
            "type": "solution",
            "severity": "hard",
            "title": "Relays Are OK — Issue Is Elsewhere",
            "image": None,
            "video": None,
            "steps": [
                "Both STO relays (K1 and K2) are working correctly — voltage in range and feedback signals active.",
                "The block on movement is coming from somewhere else in the system.",
                "Check Hardware Health for any other components showing errors (motor controller, CAN nodes, etc.).",
                "Confirm the robot is in READY state with no active errors in the notification bell.",
                "If everything appears green but the robot still won't move, contact technical support.",
                "Have ready: robot serial number, a screenshot of Hardware Health, and the exported error log (System → Error Log → Export).",
            ],
        },

        "sol_boggy_issue": {
            "type": "solution",
            "severity": "hard",
            "title": "Boggy — Mechanical Brake Not Releasing",
            "image": "assets/images/oil bogie.jpeg",
            "video": "assets/images/loose nuts old nuts.mp4",
            "steps": [
                "Current is reaching the boggy but the robot is not moving — the mechanical brake inside the boggy is not releasing.",
                "Expected current when moving: **~15A** (MiR250) or **~45A** (MiR600).",
                "Inspect the boggy for oil leaks or visible mechanical damage (see photo above).",
                "Check for loose nuts or worn components (see video above).",
                "If current is present and stuck with no movement, the boggy's internal brake is likely faulty.",
                "This typically requires boggy replacement.",
                "Contact technical support or your MiR distributor.",
            ],
        },

        "sol_motor_controller": {
            "type": "solution",
            "severity": "hard",
            "title": "Motor Controller May Be Faulty",
            "image": None,
            "video": None,
            "steps": [
                "No current is reaching the boggies despite relays appearing OK.",
                "⚠️ Before concluding motor controller fault: confirm the robot is in READY state and all obstacles are cleared (or protective fields are muted).",
                "⚠️ Nodes 3, 4 and 20 will show as red/uninitialized in protective state — this is NORMAL. Do not use those as a diagnostic signal.",
                "If the robot is in READY state with no obstacles and still no current → motor controller is likely the issue.",
                "Contact technical support for motor controller diagnosis and replacement.",
            ],
        },

        "sol_escalate": {
            "type": "solution",
            "severity": "hard",
            "title": "Issue Not Identified — Escalate to Support",
            "image": None,
            "video": None,
            "steps": [
                "Take a screenshot of the MiR web interface dashboard.",
                "Note the robot serial number (on the robot label or in the web interface).",
                "Export the error log: **System → Error Log → Export**.",
                "Contact your MiR distributor or support with: serial number, error log, and a description of what happened.",
            ],
        },
    },
}
