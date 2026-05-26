FLOW = {
    "title": "Charging Station Issues",
    "start": "q_charge_symptom",
    "nodes": {

        # ── PHASE 1: SYMPTOM ──────────────────────────────────────────────────

        "q_charge_symptom": {
            "type": "question",
            "text": "What is the charging issue you are seeing?",
            "hint": "Select the closest match to your situation.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Robot docks correctly but doesn't start charging",   "next": "q_station_powered",    "style": "warn"},
                {"label": "Robot fails to dock to the charging station",        "next": "sol_goto_docking",     "style": "warn"},
                {"label": "Robot charges but stops before 100%",               "next": "q_battery_pct",        "style": "neutral"},
            ],
        },

        # ── PATH: ROBOT DOCKED BUT NOT CHARGING ───────────────────────────────

        "q_station_powered": {
            "type": "question",
            "text": "Is the charging station powered ON and active?",
            "hint": "Check that the charging station has power (indicator lights on the station, cables connected to mains power).",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — station is powered on",  "next": "q_mission_correct",  "style": "good"},
                {"label": "No — station is off",          "next": "sol_power_station",  "style": "warn"},
            ],
        },

        "q_mission_correct": {
            "type": "question",
            "text": "Is the charging mission built correctly? Does it use a Dock action followed by a Charge action?",
            "hint": "The robot will not charge if only a Dock action is used — you must also add a Charge action after the Dock.",
            "info": (
                "Correct charging mission structure:\n"
                "1. Dock action → drives the robot to the charging station marker\n"
                "2. Charge action → tells the robot to enable the charging relay\n\n"
                "⚠️ A Dock action alone does NOT trigger charging.\n"
                "⚠️ If using MiR Fleet Auto Charging, check the known issues list for any Auto Charging bugs."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — mission has Dock then Charge",       "next": "q_battery_above_90",    "style": "good"},
                {"label": "No — Charge action is missing",            "next": "sol_add_charge_action", "style": "warn"},
            ],
        },

        "q_battery_above_90": {
            "type": "question",
            "text": "Is the robot's battery already above 90%?",
            "hint": "The charging station will not start charging if the battery is above 90%. This is normal behavior.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — battery is already above 90%",      "next": "sol_battery_full",      "style": "good"},
                {"label": "No — battery is below 90%",               "next": "q_software_version",    "style": "neutral"},
            ],
        },

        "q_software_version": {
            "type": "question",
            "text": "Is the robot software version 2.8.3 or lower?",
            "hint": "Several charging station issues were fixed in software version 2.9.0. Check in System → About.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — running 2.8.3 or lower",                "next": "sol_update_software",   "style": "warn"},
                {"label": "No — running 2.9.0 or higher",               "next": "q_charging_pads",       "style": "good"},
            ],
        },

        "q_charging_pads": {
            "type": "checklist",
            "text": "Check charging pad alignment and cleanliness",
            "hint": "The charging pads must be clean, undamaged, and properly aligned for charging to work.",
            "info": (
                "Two things to check:\n\n"
                "1. ALIGNMENT: The center of the robot's charging pad assembly must align with the center of the station's charging plate.\n"
                "   Use a mirror or camera positioned under the robot to verify pad contact.\n"
                "   If alignment is off for this one station → adjust the charging station offsets.\n"
                "   If off for ALL stations → adjust the robot's global docking offset.\n\n"
                "2. CLEANLINESS: Corroded or dirty pads prevent electrical contact.\n"
                "   See the guide 'How to clean the charging pads under MiR robots' on MiR Support Portal.\n"
                "   Also check the station's charging plate pads."
            ),
            "image": [
                "assets/images/charging pad infected.jpeg",
                "assets/images/charging pad 2.jpeg",
                "assets/images/charging pad 3.jpeg",
                "assets/images/charging pad 4.jpeg",
            ],
            "video": "assets/images/how to take video of charging pad.mp4",
            "items": [
                {
                    "key": "pads_clean",
                    "label": "Cleaned the charging pads on the robot and on the station. No corrosion or contamination visible.",
                },
                {
                    "key": "pads_aligned",
                    "label": "Verified pad alignment: robot's charging pad center is aligned with station plate center.",
                },
            ],
            "options": [
                {
                    "label": "Pads clean and aligned — still not charging",
                    "next": "q_hardware_health_charger",
                    "style": "warn",
                    "requires": ["pads_clean", "pads_aligned"],
                },
                {
                    "label": "Found dirty pads — cleaned them",
                    "next": "sol_pads_cleaned",
                    "style": "good",
                    "requires": ["pads_clean"],
                },
            ],
        },

        "q_hardware_health_charger": {
            "type": "question",
            "text": "Go to Hardware Health → Power System → Charger. What does the 'Charging status' field show while the robot is docked and the Charge action is active?",
            "hint": "The robot must be docked AND a Charge action must be running for this status to update.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Disconnected",                       "next": "q_charging_relay",     "style": "warn"},
                {"label": "Charging Phase X (with an Alarm code)", "next": "sol_charging_alarm", "style": "warn"},
                {"label": "Charging (seems to be working?)",   "next": "sol_intermittent",     "style": "neutral"},
            ],
        },

        "q_charging_relay": {
            "type": "question",
            "text": "Status shows 'Disconnected'. Go to Hardware Health → Power System → Charging Status → Charging Relay. What is the status?",
            "hint": "This tells you if the issue is on the station side or the robot side.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Charging Relay is ON",   "next": "sol_replace_station",  "style": "warn"},
                {"label": "Charging Relay is OFF",  "next": "sol_contact_support_charger", "style": "warn"},
            ],
        },

        # ── PATH: STOPS BEFORE 100% ───────────────────────────────────────────

        "q_battery_pct": {
            "type": "solution",
            "severity": "easy",
            "title": "Charging Station Stops at 90% — Normal Behavior",
            "image": None,
            "video": None,
            "steps": [
                "If the robot previously docked and charged to 100%, the charging station stops charging until the battery drops below 90% again.",
                "This is normal protective behavior — the station will resume charging automatically when the battery drops below 90%.",
                "To manually trigger a new charging session: undock the robot, let it run (consuming battery below 90%), then send it back to charge.",
                "If the robot is not reaching 90% during normal operations, check your fleet mission settings to confirm the low-battery threshold triggers a charging mission.",
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────────

        "sol_goto_docking": {
            "type": "solution",
            "severity": "medium",
            "title": "Robot Fails to Dock — Use Docking Troubleshooting Flow",
            "image": None,
            "video": None,
            "steps": [
                "The robot is not reaching the charging station correctly — this is a docking problem, not a charging problem.",
                "Go to the 'Docking Issues' troubleshooting flow.",
                "Common docking causes: wrong map active, dirty scanners, misaligned Entry position, poor map quality.",
            ],
        },

        "sol_power_station": {
            "type": "solution",
            "severity": "easy",
            "title": "Charging Station Is Off — Power It On",
            "image": None,
            "video": None,
            "steps": [
                "The charging station has no power or is switched off.",
                "Check the mains power connection to the charging station.",
                "Turn the charging station on according to its manual.",
                "Wait 30 seconds for the station to initialize, then try docking and charging again.",
                "If the station won't turn on despite having mains power, there may be a station hardware fault — contact your distributor.",
            ],
        },

        "sol_add_charge_action": {
            "type": "solution",
            "severity": "easy",
            "title": "Charging Mission Missing Charge Action",
            "image": None,
            "video": None,
            "steps": [
                "The mission is missing the Charge action — without it, the robot docks but does not enable charging.",
                "Edit the mission: after the Dock action, add a Charge action.",
                "The Charge action tells the robot to activate the charging relay.",
                "Save the mission and test again.",
                "Note: the robot must stay in place during the Charge action. Do not add a Move action immediately after.",
            ],
        },

        "sol_battery_full": {
            "type": "solution",
            "severity": "easy",
            "title": "Battery Already Above 90% — Normal Behavior",
            "image": None,
            "video": None,
            "steps": [
                "The battery is already above 90% — the charging station will not begin charging until it drops below 90%.",
                "This is normal protective behavior. The station is working correctly.",
                "To test charging: run the robot until the battery drops below 90%, then retry the charging mission.",
            ],
        },

        "sol_update_software": {
            "type": "solution",
            "severity": "medium",
            "title": "Update Robot Software to 2.9.0 or Higher",
            "image": None,
            "video": None,
            "steps": [
                "Software version 2.8.3 and lower have known charging issues that were fixed in version 2.9.0.",
                "In the robot interface, go to System → Software Update.",
                "Follow the update wizard to upgrade to the latest available version.",
                "After updating and restarting, test the charging station again.",
                "If a software update introduced the charging issue (regression), contact MiR Technical Support.",
            ],
        },

        "sol_pads_cleaned": {
            "type": "solution",
            "severity": "easy",
            "title": "Dirty Charging Pads Cleaned — Test Again",
            "image": None,
            "video": None,
            "steps": [
                "Dirty or corroded charging pads prevent electrical contact between the robot and station.",
                "After cleaning both the robot pads and the station plate, dock the robot again.",
                "Watch the Charging status in Hardware Health → Power System → Charger.",
                "Schedule regular pad cleaning as part of preventive maintenance.",
                "See the guide 'How to clean the charging pads under MiR robots' on MiR Support Portal.",
            ],
        },

        "sol_replace_station": {
            "type": "solution",
            "severity": "hard",
            "title": "Charging Status Disconnected with Relay ON — Replace Charging Station",
            "image": None,
            "video": None,
            "steps": [
                "The charging relay is ON (robot is trying to charge) but the Charging status shows Disconnected.",
                "This indicates the charging station is not delivering power despite the relay being active.",
                "First verify pad cleanliness and alignment — see the guide 'How to clean the charging pads under MiR robots'.",
                "If pads are clean and aligned but charging still fails → the charging station hardware is faulty.",
                "Replace the charging station or contact MiR Technical Support / your distributor.",
                "Include in your support ticket: robot serial number, Charging status screenshot, which station is affected.",
            ],
        },

        "sol_charging_alarm": {
            "type": "solution",
            "severity": "hard",
            "title": "Charging Alarm Code Reported",
            "image": None,
            "video": None,
            "steps": [
                "The robot is reporting a charging alarm code in Hardware Health → Power System → Charger → Alarm.",
                "Note the exact alarm code displayed.",
                "Contact MiR Technical Support and include:",
                "• Robot serial number",
                "• Screenshot of Hardware Health → Power System → Charger with the Alarm code visible",
                "• Description of what happens when the robot tries to charge",
            ],
        },

        "sol_intermittent": {
            "type": "solution",
            "severity": "medium",
            "title": "Charging Appears Active but Is Intermittent",
            "image": None,
            "video": None,
            "steps": [
                "The Charging status shows charging is active, but in practice charging is unreliable or stops prematurely.",
                "Check pad alignment while the robot is docked: pads must be centered on the station plate.",
                "Monitor the battery percentage over time to confirm whether charging is actually progressing.",
                "If charging starts and stops: pads may be making intermittent contact. Check for vibrations or loose pad mounting.",
                "If the issue persists, contact MiR Technical Support with the robot serial number and a description of the behavior.",
            ],
        },

        "sol_contact_support_charger": {
            "type": "solution",
            "severity": "hard",
            "title": "Charging Relay OFF — Escalate to Support",
            "image": None,
            "video": None,
            "steps": [
                "The Charging status shows Disconnected AND the Charging Relay is OFF.",
                "This means the robot is not activating the charging relay at all — a software or hardware fault.",
                "First confirm the mission has a Charge action (not just Dock).",
                "Also check if any top module features are blocking the charging function (System → Settings → Features).",
                "If everything appears correct, contact MiR Technical Support.",
                "Include: robot serial number, screenshot of Hardware Health → Charger, mission screenshot.",
            ],
        },
    },
}
