FLOW = {
    "title": "Constantly in Protective State",
    "start": "q_stop_type",
    "nodes": {

        # ── PHASE 1: IDENTIFY STOP TYPE ──────────────────────────────────────

        "q_stop_type": {
            "type": "question",
            "text": "Is the robot in Emergency Stop or Protective Stop?",
            "hint": "Check the top status bar in the web interface — it shows the current state.",
            "info": (
                "How to identify:\n"
                "• Emergency Stop: web interface shows 'EMERGENCY STOP'. Usually caused by an E-stop button being pressed.\n"
                "• Protective Stop: web interface shows 'PROTECTIVE STOP'. Usually caused by laser scanners detecting an obstacle or a system error.\n\n"
                "Go to Monitoring → Hardware Health → Safety System to see which specific field triggered the stop."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Emergency Stop",           "next": "q_estop_buttons",  "style": "warn"},
                {"label": "Protective Stop",          "next": "q_key_auto",       "style": "warn"},
                {"label": "Not sure — both or other", "next": "q_estop_buttons",  "style": "neutral"},
            ],
        },

        # ── E-STOP PATH ───────────────────────────────────────────────────────

        "q_estop_buttons": {
            "type": "question",
            "text": "Are ALL Emergency Stop buttons physically released (twisted or pulled out)?",
            "hint": "Check all E-stop buttons on the robot body. Also check any external E-stop devices connected to the robot.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — all E-stops are released",   "next": "q_key_auto",        "style": "good"},
                {"label": "No — one is still pressed/engaged", "next": "sol_release_estop", "style": "warn"},
            ],
        },

        # ── COMMON PATH: KEY & BRAKE ──────────────────────────────────────────

        "q_key_auto": {
            "type": "question",
            "text": "Is the Operating Mode key switch set to AUTOMATIC?",
            "hint": "The key selector is on the side or back of the robot. In MANUAL mode the robot stays in protective stop and will not ask for Reset.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — key is in AUTOMATIC",  "next": "q_brake_switch",  "style": "good"},
                {"label": "No — key is in MANUAL",      "next": "sol_key_to_auto", "style": "warn"},
            ],
        },

        "q_brake_switch": {
            "type": "question",
            "text": "Is the Manual Brake Release switch set to OFF (not active)?",
            "hint": "This is a two-position switch on the back of the robot. If ON, the robot enters Protective Stop and cannot operate.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — brake release switch is OFF", "next": "q_slow_driving",   "style": "good"},
                {"label": "No — brake release switch is ON",   "next": "sol_brake_switch", "style": "warn"},
            ],
        },

        # ── SCANNER BEHAVIOR ──────────────────────────────────────────────────

        "q_slow_driving": {
            "type": "question",
            "text": "Before entering Protective Stop — was the robot driving slowly, stopping-and-going, or detecting phantom obstacles?",
            "hint": "In the web interface you can see red dots on the map. If there are many red dots where there are no real obstacles, the scanner is misbehaving.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — stop-and-go or phantom obstacles",   "next": "q_environment",  "style": "warn"},
                {"label": "No — robot stopped suddenly and stays",    "next": "q_safety_health", "style": "neutral"},
            ],
        },

        "q_environment": {
            "type": "checklist",
            "text": "Check for scanner interference in the environment",
            "hint": "Laser scanners can be fooled by reflective, transparent, or shiny surfaces near the floor.",
            "image": "assets/images/scanner clean.jpeg",
            "video": None,
            "info": (
                "Common causes of phantom obstacle detection:\n"
                "• Reflective, shiny, or transparent material within 200 mm of the floor\n"
                "  (e.g., metal shelves, shiny loads, glass walls, plastic curtains)\n"
                "• Direct lighting aimed at scanner level\n"
                "• Dirty or scratched scanner lens\n"
                "• Scanner making mechanical grinding noises\n\n"
                "Check the map view in the web interface — red dots show what the scanners detect."
            ),
            "items": [
                {
                    "key": "scanner_clean",
                    "label": "Cleaned the laser scanner lenses with a clean anti-static cloth — no scratches or damage visible.",
                },
                {
                    "key": "env_check",
                    "label": "Checked the operating area: no reflective, transparent, or shiny surfaces within 200 mm of the floor along the robot's path.",
                },
            ],
            "options": [
                {
                    "label": "Found and fixed the issue (dirty scanner or reflective surface)",
                    "next": "sol_environment_fixed",
                    "style": "good",
                    "requires": ["scanner_clean", "env_check"],
                },
                {
                    "label": "Environment looks OK — problem continues",
                    "next": "q_scanner_display",
                    "style": "warn",
                },
            ],
        },

        # ── HARDWARE HEALTH CHECK ─────────────────────────────────────────────

        "q_safety_health": {
            "type": "question",
            "text": "In the web interface go to Monitoring → Hardware Health → Safety System. Is there a specific field showing an error (not green)?",
            "hint": "Green = OK. Red or showing 'Error' = problem. Check: E-stop, STO Feedback, Mechanical brake feedback, Turn speed violation.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — I can see a specific error field",  "next": "q_specific_error",  "style": "warn"},
                {"label": "No — all fields appear green/normal",     "next": "q_scanner_display", "style": "neutral"},
            ],
        },

        "q_specific_error": {
            "type": "question",
            "text": "Which error is reported in Hardware Health → Safety System?",
            "hint": "Select the closest match to what you see in the interface.",
            "image": None,
            "video": None,
            "options": [
                {"label": "STO Feedback or STO Relay error",       "next": "sol_sto_error",      "style": "warn"},
                {"label": "Mechanical brake feedback",             "next": "sol_brake_feedback", "style": "warn"},
                {"label": "Turn speed violation",                  "next": "sol_turn_speed",     "style": "warn"},
                {"label": "Emergency button / E-stop input error", "next": "sol_estop_wiring",   "style": "warn"},
            ],
        },

        # ── SCANNER DISPLAY CHECK ─────────────────────────────────────────────

        "q_scanner_display": {
            "type": "question",
            "text": "Open the robot covers and check the small display on each safety laser scanner. What does it show?",
            "hint": "MiR250: remove front and rear covers. MiR600/1350: remove front-left and rear-right corner covers. Robot must be ON.",
            "image": [
                "assets/images/glass cover.jpeg",
                "assets/images/scanner F2 fault.jpg",
                "assets/images/scanner E1 fault.jpg",
            ],
            "video": None,
            "info": (
                "Scanner display meanings:\n"
                "• Green checkmarks, red crosses, or yellow warnings → scanner communicating, continue below\n"
                "• F2 fault → software needs updating to v2.10.3 or higher\n"
                "• E1 fault → temporary connection error, restart the robot\n"
                "• Blank (off) → power supply issue to the scanner\n\n"
                "⚠️ Be careful of exposed electrical cables when opening covers."
            ),
            "options": [
                {"label": "Shows checks, crosses, or warnings",       "next": "q_ping_scanners",    "style": "neutral"},
                {"label": "Shows F2 fault",                           "next": "sol_update_f2",      "style": "warn"},
                {"label": "Shows E1 fault",                           "next": "sol_restart_e1",     "style": "warn"},
                {"label": "Blank — one or both scanners are off",     "next": "q_one_scanner_off",  "style": "warn"},
            ],
        },

        "q_ping_scanners": {
            "type": "question",
            "text": "Can you ping both laser scanners?",
            "hint": "Connect to robot WiFi access point or service port. Open Command Prompt and ping both scanner IPs.",
            "info": (
                "Open Command Prompt and run:\n"
                "  ping 192.168.12.10   (front scanner)\n"
                "  ping 192.168.12.11   (rear scanner)\n\n"
                "A successful ping returns replies for most of the 4 packets.\n"
                "On MiR250 you can also check the network indicator on the scanner display itself."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — both scanners respond to ping",    "next": "sol_sick_report",   "style": "good"},
                {"label": "No — one or both scanners don't respond", "next": "sol_scanner_cable", "style": "warn"},
            ],
        },

        "q_one_scanner_off": {
            "type": "question",
            "text": "Is only ONE scanner display off, or are BOTH off?",
            "hint": "One off = likely power cable issue to that scanner. Both off = power board or safety PLC issue.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Only one scanner is off",  "next": "sol_scanner_power_single", "style": "warn"},
                {"label": "Both scanners are off",    "next": "q_plc_power_log",          "style": "warn"},
            ],
        },

        "q_plc_power_log": {
            "type": "question",
            "text": "Go to Monitoring → System Log and search for the message 'Iso24VPlc: PGood failed'. Is it present?",
            "hint": "This message means the power board is not delivering 24V to the safety PLC and/or scanners.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — message is in the log",   "next": "sol_power_board_resistance", "style": "warn"},
                {"label": "No — message not found",        "next": "sol_measure_voltage",        "style": "neutral"},
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────────

        "sol_release_estop": {
            "type": "solution",
            "severity": "easy",
            "title": "Emergency Stop Button Still Active",
            "image": None,
            "video": None,
            "steps": [
                "Locate the pressed Emergency Stop button (E-stop).",
                "Release it by **twisting clockwise** or **pulling it out**, depending on the button model.",
                "Check ALL E-stop buttons on the robot — there may be more than one.",
                "Also check any external E-stop devices connected to the robot (portable E-stops, door switches, safety gates).",
                "Once all E-stops are released, the blue Reset button should flash → press it.",
                "Press Play in the web interface → green lights = ready.",
            ],
        },

        "sol_key_to_auto": {
            "type": "solution",
            "severity": "easy",
            "title": "Operating Mode Key Is in MANUAL",
            "image": None,
            "video": None,
            "steps": [
                "Turn the Operating Mode key switch to the **AUTOMATIC** position.",
                "Wait a few seconds — the robot should ask you to press the Reset button.",
                "Press the blue Reset button → yellow lights (paused) → press Play → green lights = ready.",
                "If the robot still doesn't ask for Reset after switching to Automatic, check Hardware Health for other errors.",
            ],
        },

        "sol_brake_switch": {
            "type": "solution",
            "severity": "easy",
            "title": "Manual Brake Release Switch Is Active",
            "image": None,
            "video": None,
            "steps": [
                "Locate the Manual Brake Release switch on the back of the robot.",
                "Flip the switch to the **OFF** position.",
                "Open the web interface → tap the bell icon (notifications) → find and clear the Sanity Check Error.",
                "The blue Reset button should now flash → press it.",
                "Yellow lights → press Play → green lights = ready.",
            ],
        },

        "sol_environment_fixed": {
            "type": "solution",
            "severity": "easy",
            "title": "Scanner Interference — Environment Issue Resolved",
            "image": None,
            "video": None,
            "steps": [
                "The phantom obstacles or stop-and-go behavior was caused by scanner contamination or an environmental reflector.",
                "After cleaning the scanner and/or removing the reflective/transparent material, test the robot again.",
                "The robot should now navigate without false protective stops.",
                "Schedule regular scanner cleaning as part of preventive maintenance.",
                "If the issue returns, look for new reflective surfaces or changes in the operating area.",
            ],
        },

        "sol_sto_error": {
            "type": "solution",
            "severity": "hard",
            "title": "STO Relay Feedback Error",
            "image": [
                "assets/images/Relay K1 mir250.jpeg",
                "assets/images/relay mir600.jpeg",
            ],
            "video": None,
            "steps": [
                "The STO (Safe Torque Off) relay is reporting a feedback error — the PLC is not receiving the relay confirmation signal.",
                "Go to: Monitoring → Hardware Health → Safety System → STO Feedback to confirm the error.",
                "Measure the voltage at K1 and K2 relay terminals with robot in READY state — expected **47–52 V**.",
                "If voltage is out of range: try the relay manual override button — press it **ONCE only**. Pressing multiple times triggers another lockout error.",
                "If voltage is correct but error persists: the relay's internal feedback contact may be worn. The relay needs replacement.",
                "Contact technical support with: robot serial number, which relay (K1/K2), and the voltage readings.",
            ],
        },

        "sol_brake_feedback": {
            "type": "solution",
            "severity": "hard",
            "title": "Mechanical Brake Feedback Error",
            "image": None,
            "video": None,
            "steps": [
                "The mechanical brake relay feedback is failing — the PLC is not receiving the expected confirmation from the brake relay.",
                "Go to: Monitoring → Hardware Health → Safety System → Mechanical brake feedback to confirm.",
                "Check the wiring connections at the brake relay terminals — look for loose or damaged wires.",
                "If wiring looks intact, the relay may be faulty and needs replacement.",
                "Contact technical support with the robot serial number and a screenshot of Hardware Health.",
            ],
        },

        "sol_turn_speed": {
            "type": "solution",
            "severity": "medium",
            "title": "Turn Speed Violation",
            "image": None,
            "video": None,
            "steps": [
                "The robot stopped because the rotational speed difference between the drive wheels was too great.",
                "This typically points to a problem with one of the drive bogeys or wheels.",
                "Check: are both drive wheels clean and able to rotate freely?",
                "Check: is there any mechanical damage to a bogey?",
                "Run an encoder test: in the web interface go to System → Diagnostics → Encoder test.",
                "If one wheel consistently drives more than the other, the bogey or encoder may need inspection or replacement.",
                "Contact technical support if the issue persists.",
            ],
        },

        "sol_estop_wiring": {
            "type": "solution",
            "severity": "hard",
            "title": "Emergency Stop Circuit Error",
            "image": None,
            "video": None,
            "steps": [
                "The Safety System reports an error with the Emergency Stop input circuit.",
                "Check: are all E-stop buttons properly released and undamaged?",
                "Check any external E-stop devices or safety circuits connected to the robot's auxiliary interface.",
                "Inspect the E-stop wiring for damaged, loose, or disconnected cables.",
                "If wiring is intact but the error persists, the E-stop circuit has a component failure.",
                "Contact technical support with: serial number and a screenshot of Hardware Health → Safety System.",
            ],
        },

        "sol_sick_report": {
            "type": "solution",
            "severity": "hard",
            "title": "Scanners Connected but Safety System Error Persists",
            "image": None,
            "video": None,
            "steps": [
                "Both laser scanners respond to ping (connected), but the Safety System is still reporting an error.",
                "Generate a SICK report: in the web interface go to System → SICK Report.",
                "Also export the error log: System → Error Log → Export.",
                "Contact MiR Technical Support with: robot serial number, SICK report file, and error log.",
                "Note: If the scanner display shows red crosses or warnings, refer to SICK fault documentation for your scanner model (microScan3 for MiR600/1350, nanoScan3 for MiR250).",
            ],
        },

        "sol_scanner_cable": {
            "type": "solution",
            "severity": "hard",
            "title": "Safety Laser Scanner Not Responding to Ping",
            "image": None,
            "video": None,
            "steps": [
                "One or both scanners are not connected (not responding at 192.168.12.10 or .11).",
                "Check the Ethernet cable connecting the scanner to the robot's internal network switch.",
                "For MiR250: see the guide 'How to replace the safety laser scanner cables on MiR250' (MiR Support Portal).",
                "For MiR600/1350: check the Ethernet connectors behind the safety laser scanner.",
                "Try a different Ethernet cable if one is available.",
                "If cable is fine but scanner still doesn't ping, the scanner itself may be faulty and needs replacement.",
                "Contact technical support with: robot serial number and which scanner (front/rear) is not responding.",
            ],
        },

        "sol_scanner_power_single": {
            "type": "solution",
            "severity": "hard",
            "title": "One Scanner Off — Power Cable Issue",
            "image": None,
            "video": None,
            "steps": [
                "Only one scanner display is off — this indicates a power supply issue to that specific scanner.",
                "For MiR250: check the power cable behind the affected safety laser scanner. See the guide 'How to replace the safety laser scanner cables on MiR250'.",
                "For MiR600/1350: check the J3 connector on the power board and the power connector behind each scanner.",
                "Remove the robot's top cover to access the back of the safety laser scanners.",
                "Ensure the power cable is firmly connected at both ends.",
                "If firmly connected but scanner still won't power on, the cable or scanner may need replacement.",
            ],
        },

        "sol_power_board_resistance": {
            "type": "solution",
            "severity": "hard",
            "title": "Power Board Not Delivering 24V — Measure Resistance",
            "image": None,
            "video": None,
            "steps": [
                "'Iso24VPlc: PGood failed' means the power board is not delivering 24V to the safety system.",
                "Turn the robot OFF and disconnect the battery before measuring resistance.",
                "For MiR250: Unplug the 6-pin Molex PLC power connector. Measure resistance between pin pairs: 1-2 (PLC), 3-4 (rear scanner), 5-6 (front scanner).",
                "For MiR600/1350: Unplug the J3 connector from the power board. Measure between pairs: 7-8 (front scanner), 9-10 (rear scanner), 16-17 (PLC).",
                "Any pair measuring **0–5 Ω** indicates a short circuit in that component — replace it.",
                "If the same pairs on the power board itself measure 0–5 Ω → replace the power board.",
                "Contact technical support with measurement results and robot serial number.",
            ],
        },

        "sol_measure_voltage": {
            "type": "solution",
            "severity": "hard",
            "title": "Both Scanners Off — Measure Power Board Output Voltage",
            "image": None,
            "video": None,
            "steps": [
                "Both scanner displays are off. Measure the voltage from the power board to the safety PLC (robot must be ON).",
                "For MiR250: Unplug the 6-pin Molex PLC power connector. Measure between pin pairs: 1-2 (PLC), 3-4 (rear scanner), 5-6 (front scanner). Expected: **24V** on all pairs.",
                "For MiR600/1350: Unplug the A1 and A2 wires from the safety PLC. Measure voltage between each A1 and A2 pair. Expected: **24V**.",
                "If any pair reads 0V: check the cable from the power board to the safety PLC. If cable is fine → replace the power board.",
                "If all pairs read 24V: continue to resistance measurement or contact technical support.",
                "Contact MiR Technical Support with: robot serial number and your voltage measurement results.",
            ],
        },

        "sol_update_f2": {
            "type": "solution",
            "severity": "medium",
            "title": "Scanner Shows F2 Fault — Update Software",
            "image": "assets/images/scanner F2 fault.jpg",
            "video": None,
            "steps": [
                "An F2 fault on the scanner display means the robot software needs to be updated to v2.10.3 or higher.",
                "In the robot interface: go to System → Software Update and follow the instructions.",
                "After updating, restart the robot and check if the F2 fault is cleared.",
                "If the robot is already running v2.10.3 or higher and still shows F2, contact MiR Technical Support.",
            ],
        },

        "sol_restart_e1": {
            "type": "solution",
            "severity": "easy",
            "title": "Scanner Shows E1 Fault — Restart Robot",
            "image": "assets/images/scanner E1 fault.jpg",
            "video": None,
            "steps": [
                "An E1 fault is a device error caused by a temporary connection issue between the robot and scanner.",
                "Turn the robot OFF, wait 10 seconds, then turn it ON again.",
                "After startup, check the scanner display — the E1 fault should be cleared.",
                "If the E1 fault persists after restarting, the scanner's Ethernet cable may be loose or faulty.",
                "Check the scanner Ethernet cable connection and restart again.",
            ],
        },
    },
}
