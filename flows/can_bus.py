FLOW = {
    "title": "CAN Bus / Lights Not Working",
    "start": "q_can_symptoms",
    "nodes": {

        # ── PHASE 1: CONFIRM CAN BUS ISSUE ────────────────────────────────────

        "q_can_symptoms": {
            "type": "question",
            "text": "What symptoms are you seeing?",
            "hint": "CAN bus issues can affect driving, proximity sensors, and indicator lights.",
            "info": (
                "The CAN bus connects proximity sensors, indicator lights, and the motor controller carrier board to the power board.\n"
                "If one node disconnects, it can affect the entire line.\n\n"
                "To verify a CAN bus issue:\n"
                "Go to Monitoring → Hardware Health → Powerboard → CAN Communication Bus → CAN bus MC light proxy gpio\n"
                "Check the Transmit Error Counter (TEC) and Receive Error Counter (REC).\n"
                "If TEC or REC is anything other than 0 → there is a CAN bus communication fault."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Robot cannot drive (not in protective stop)",      "next": "q_tec_rec_counters", "style": "warn"},
                {"label": "Indicator lights not working correctly",           "next": "q_tec_rec_counters", "style": "warn"},
                {"label": "Proximity sensors not working",                    "next": "q_tec_rec_counters", "style": "warn"},
                {"label": "Confirmed: TEC/REC counters are not 0",           "next": "q_robot_model",      "style": "warn"},
            ],
        },

        "q_tec_rec_counters": {
            "type": "question",
            "text": "Go to Monitoring → Hardware Health → Powerboard → CAN Communication Bus → CAN bus MC light proxy gpio. What do the TEC and REC error counters show?",
            "hint": "TEC = Transmit Error Counter. REC = Receive Error Counter. Both should be 0 when the CAN bus is healthy.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Both TEC and REC are 0 (no CAN error)",           "next": "sol_not_can_issue",   "style": "good"},
                {"label": "One or both are NOT 0 (CAN bus error confirmed)", "next": "q_robot_model",       "style": "warn"},
            ],
        },

        "q_robot_model": {
            "type": "question",
            "text": "Which robot model are you troubleshooting?",
            "hint": "The CAN bus node order and components differ between MiR250 and MiR600/MiR1350.",
            "image": None,
            "video": None,
            "options": [
                {"label": "MiR250",                  "next": "q_mir250_prep",       "style": "neutral"},
                {"label": "MiR600 or MiR1350",       "next": "q_mir600_prep",       "style": "neutral"},
            ],
        },

        # ── MiR250 PROCEDURE ───────────────────────────────────────────────────

        "q_mir250_prep": {
            "type": "checklist",
            "text": "MiR250 — Prepare for CAN Bus Diagnosis",
            "hint": "You must isolate each node one at a time to find which one is causing the error.",
            "info": (
                "The principle: disconnect ALL CAN bus devices, then reconnect them ONE AT A TIME.\n"
                "Between each connection, turn the robot on, check TEC/REC counters, then turn it off before connecting the next.\n\n"
                "Preparation:\n"
                "1. Disconnect the battery.\n"
                "2. Remove all side covers and the top cover.\n"
                "3. Locate the PCB board.\n\n"
                "⚠️ Work with battery disconnected at all times except when checking counters.\n"
                "⚠️ Be careful of exposed electrical cables."
            ),
            "image": None,
            "video": None,
            "items": [
                {"key": "battery_off",   "label": "Battery is disconnected."},
                {"key": "covers_off",    "label": "All side covers and top cover are removed."},
                {"key": "pcb_located",   "label": "PCB board is located and accessible."},
            ],
            "options": [
                {
                    "label": "Prepared — ready to start diagnosis",
                    "next": "q_mir250_step1",
                    "style": "good",
                    "requires": ["battery_off", "covers_off", "pcb_located"],
                },
            ],
        },

        "q_mir250_step1": {
            "type": "question",
            "text": "MiR250 Step 1: Disconnect CAB-007 from the J2 socket on the PCB. Reconnect the battery, turn the robot on, and check TEC/REC. Are both counters 0?",
            "hint": "If counters are still not 0 with CAB-007 disconnected, the power board or PCB itself is the fault.",
            "image": "assets/images/switch diodes MiR250.jpg",
            "video": None,
            "options": [
                {"label": "No — counters still not 0 (power board/PCB fault)",  "next": "sol_can_power_board",    "style": "warn"},
                {"label": "Yes — counters are now 0 (fault is in CAN devices)",  "next": "q_mir250_step2",         "style": "good"},
            ],
        },

        "q_mir250_step2": {
            "type": "checklist",
            "text": "MiR250 Step 2: Disconnect all proximity board CAN connections",
            "hint": "Disconnect J3 and J4 on all eight proximity modules — these are the two right-most connectors when seen from above, facing the inner side.",
            "info": (
                "Steps:\n"
                "1. Turn off robot and disconnect battery.\n"
                "2. Reconnect CAB-007 to J2 socket.\n"
                "3. On each of the 8 proximity modules, disconnect the CAN bus cables in socket J3 and J4.\n"
                "   ⚠️ These are always the two right-most connectors (from above, facing the inner side).\n"
                "   ⚠️ Label each cable or take a photo before disconnecting — you must reconnect them correctly.\n"
                "4. Reconnect battery, turn on robot, check TEC/REC counters."
            ),
            "image": None,
            "video": None,
            "items": [
                {"key": "cab007_reconnected",   "label": "Reconnected CAB-007 to J2 socket on PCB."},
                {"key": "all_prox_disconnected", "label": "Disconnected J3 and J4 from all 8 proximity modules. Labeled or photographed connections."},
            ],
            "options": [
                {
                    "label": "Done — reconnected battery and checking counters",
                    "next": "q_mir250_step2_result",
                    "style": "neutral",
                    "requires": ["cab007_reconnected", "all_prox_disconnected"],
                },
            ],
        },

        "q_mir250_step2_result": {
            "type": "question",
            "text": "With CAB-007 reconnected and all proximity boards disconnected, are TEC and REC counters both 0?",
            "hint": "If not 0 now → the motor controller carrier board is the fault. If 0 → the fault is in one of the proximity boards.",
            "image": None,
            "video": None,
            "options": [
                {"label": "No — counters still not 0 (motor controller board fault)", "next": "sol_can_motor_controller", "style": "warn"},
                {"label": "Yes — counters are 0 (fault is in a proximity board)",     "next": "q_mir250_add_boards",     "style": "good"},
            ],
        },

        "q_mir250_add_boards": {
            "type": "question",
            "text": "MiR250 Step 3: Reconnect proximity boards ONE BY ONE. After each one, turn on the robot and check TEC/REC. Did the counters go non-zero after adding a specific board?",
            "hint": "Follow the MiR250 wiring diagram for the correct connection order of proximity boards (available on MiR Support Portal).",
            "info": (
                "Process:\n"
                "1. Turn off robot, disconnect battery.\n"
                "2. Reconnect the NEXT proximity board in the CAN bus connection line.\n"
                "3. Reconnect battery, turn on robot, check TEC/REC.\n"
                "4. If counters are 0: turn off, disconnect battery, add the next board. Repeat.\n"
                "5. If counters go non-zero: the last board added is the fault.\n\n"
                "See the MiR250 CAN bus connection order image in the troubleshooting guide."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — found the faulty proximity board",          "next": "sol_can_resolving",    "style": "warn"},
                {"label": "No — all boards reconnected and counters stay 0", "next": "sol_can_connectors_ok", "style": "good"},
            ],
        },

        # ── MiR600/1350 PROCEDURE ──────────────────────────────────────────────

        "q_mir600_prep": {
            "type": "checklist",
            "text": "MiR600/1350 — Prepare for CAN Bus Diagnosis",
            "hint": "Same principle: disconnect all, reconnect one at a time, check TEC/REC between each.",
            "info": (
                "Preparation:\n"
                "1. Disconnect the battery.\n"
                "2. Remove the top cover.\n\n"
                "⚠️ Work with battery disconnected at all times except when checking counters."
            ),
            "image": None,
            "video": None,
            "items": [
                {"key": "battery_off",    "label": "Battery is disconnected."},
                {"key": "top_cover_off",  "label": "Top cover is removed."},
            ],
            "options": [
                {
                    "label": "Prepared — ready to start",
                    "next": "q_mir600_step1",
                    "style": "good",
                    "requires": ["battery_off", "top_cover_off"],
                },
            ],
        },

        "q_mir600_step1": {
            "type": "checklist",
            "text": "MiR600/1350 Step 1: Disconnect all proximity boards and GPIO board",
            "hint": "Disconnect CAN bus cables J3 and J4 on ALL proximity modules, and J4 and J5 on the GPIO board (behind the power board).",
            "info": (
                "Steps:\n"
                "1. On each proximity module: disconnect CAN bus cables from J3 and J4.\n"
                "   (Right-most connectors, facing the inner side)\n"
                "   ⚠️ Label cables or use the MiR600/MiR1350 wiring diagram for correct reconnection.\n"
                "2. Locate the GPIO board (behind the power board).\n"
                "3. Disconnect cables from J4 and J5 sockets on the GPIO board.\n"
                "4. Reconnect battery, turn on robot, check TEC/REC counters."
            ),
            "image": None,
            "video": None,
            "items": [
                {"key": "prox_disconnected", "label": "Disconnected J3 and J4 from ALL proximity modules. Labeled or photographed connections."},
                {"key": "gpio_disconnected", "label": "Disconnected J4 and J5 from the GPIO board (behind power board)."},
            ],
            "options": [
                {
                    "label": "Done — checking TEC/REC counters",
                    "next": "q_mir600_step1_result",
                    "style": "neutral",
                    "requires": ["prox_disconnected", "gpio_disconnected"],
                },
            ],
        },

        "q_mir600_step1_result": {
            "type": "question",
            "text": "With all proximity boards and GPIO board disconnected, are TEC and REC counters both 0?",
            "hint": "If not 0 → the power board is the fault. If 0 → reconnect the GPIO board next.",
            "image": None,
            "video": None,
            "options": [
                {"label": "No — counters still not 0 (power board fault)",      "next": "sol_can_power_board",    "style": "warn"},
                {"label": "Yes — counters are 0 (reconnect GPIO board next)",   "next": "q_mir600_gpio",          "style": "good"},
            ],
        },

        "q_mir600_gpio": {
            "type": "question",
            "text": "Reconnect cables to J4 and J5 on the GPIO board. Turn on robot. Are TEC/REC still 0?",
            "hint": "If they go non-zero after reconnecting the GPIO board → the GPIO board is the fault.",
            "image": None,
            "video": None,
            "options": [
                {"label": "No — counters went non-zero (GPIO board fault)",     "next": "sol_can_gpio_board",   "style": "warn"},
                {"label": "Yes — still 0 (fault is in a proximity board)",      "next": "q_mir600_add_boards",  "style": "good"},
            ],
        },

        "q_mir600_add_boards": {
            "type": "question",
            "text": "Reconnect proximity boards ONE BY ONE following the CAN bus connection order. Did adding a specific board make TEC/REC go non-zero?",
            "hint": "Turn off and disconnect battery before each addition. Turn on and check counters after each one. Follow the MiR600/MiR1350 wiring diagram for connection order.",
            "info": (
                "Process:\n"
                "1. Turn off robot, disconnect battery.\n"
                "2. Reconnect the next proximity board in the CAN bus line (follow wiring diagram).\n"
                "3. Reconnect battery, turn on robot, check TEC/REC.\n"
                "4. If 0: turn off, disconnect battery, add next board. Repeat.\n"
                "5. If non-zero: the last board added is the fault.\n\n"
                "Cables on MiR600/1350 are labeled with which socket they connect to."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — found the faulty proximity board",           "next": "sol_can_resolving",    "style": "warn"},
                {"label": "No — all boards connected and counters stay at 0", "next": "sol_can_connectors_ok", "style": "good"},
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────────

        "sol_not_can_issue": {
            "type": "solution",
            "severity": "medium",
            "title": "TEC/REC Counters Are 0 — Not a CAN Bus Fault",
            "image": None,
            "video": None,
            "steps": [
                "The CAN bus error counters are both 0, meaning the CAN bus communication is healthy.",
                "The symptoms you're seeing have a different cause:",
                "• Robot cannot drive → check the 'Robot Cannot Move' flow or 'Constantly in Protective State' flow",
                "• Indicator lights not working → check wiring to the light strips; try restarting the robot (power off/on)",
                "• Proximity sensors not working → check sensor connections and see if robot software is up to date",
                "If Hardware Health shows any errors, use those to guide further diagnosis.",
            ],
        },

        "sol_can_power_board": {
            "type": "solution",
            "severity": "hard",
            "title": "Power Board Is Causing CAN Bus Error",
            "image": None,
            "video": None,
            "steps": [
                "With all CAN bus devices disconnected, the TEC/REC counters are still non-zero — the power board itself is the fault.",
                "First check all CAN bus cables connected directly to the power board — look for:",
                "• Loose connectors at either end",
                "• Swapped polarity (reversed wires)",
                "• Damaged or modified cables",
                "If all connections look correct and secure, the power board likely needs replacement.",
                "Contact MiR Technical Support with: robot serial number, description of diagnosis steps, and TEC/REC readings.",
            ],
        },

        "sol_can_motor_controller": {
            "type": "solution",
            "severity": "hard",
            "title": "Motor Controller Carrier Board Is Causing CAN Bus Error",
            "image": None,
            "video": None,
            "steps": [
                "With CAB-007 reconnected and all proximity boards disconnected, the TEC/REC are still non-zero.",
                "The motor controller carrier board is causing the CAN bus fault.",
                "Check the CAN bus cable connecting the motor controller carrier board — look for loose, damaged, or swapped connections.",
                "If the cable looks fine, the motor controller carrier board likely needs replacement.",
                "Contact MiR Technical Support with: robot serial number and diagnostic results.",
            ],
        },

        "sol_can_gpio_board": {
            "type": "solution",
            "severity": "hard",
            "title": "GPIO Board Is Causing CAN Bus Error (MiR600/1350)",
            "image": None,
            "video": None,
            "steps": [
                "Reconnecting the GPIO board caused the TEC/REC counters to go non-zero — the GPIO board is the fault.",
                "First check the cable connections at J4 and J5 on the GPIO board for:",
                "• Loose connectors",
                "• Swapped polarity",
                "• Physical damage",
                "If cables look intact and correctly connected, the GPIO board itself is faulty and needs replacement.",
                "Contact MiR Technical Support with: robot serial number and diagnostic results.",
            ],
        },

        "sol_can_resolving": {
            "type": "solution",
            "severity": "medium",
            "title": "Faulty Proximity Board or Connection Found",
            "image": None,
            "video": None,
            "steps": [
                "Adding a specific proximity board made the TEC/REC counters go non-zero.",
                "The fault is most often a loose or incorrectly connected CAN bus cable, not the board itself.",
                "Step 1: Double-check all cable connections on the board just added — especially both ends of each cable.",
                "Step 2: Check for swapped polarity on any of the connections.",
                "Step 3: Verify the cables are connected to the correct sockets (J3 and J4, not J1/J2).",
                "Step 4: Check the cable between this board and the previous one for damage.",
                "If all connections are correct and secure, the proximity board itself likely needs replacement.",
                "Contact MiR Technical Support with: robot serial number, which node number is faulty, and what you checked.",
            ],
        },

        "sol_can_connectors_ok": {
            "type": "solution",
            "severity": "easy",
            "title": "CAN Bus Issue Resolved by Reseating Connectors",
            "image": None,
            "video": None,
            "steps": [
                "All proximity boards have been reconnected and the TEC/REC counters remain at 0.",
                "The issue was caused by a loose connection that was corrected when you reseated the connectors.",
                "Test the robot: verify it can drive, that lights work, and proximity sensors are responding.",
                "Check Monitoring → Hardware Health to confirm everything is healthy.",
                "Monitor the robot over the next few days — if the CAN bus error returns, one of the connections is intermittently loose.",
                "If the error returns, follow the same diagnosis procedure and pay extra attention to any connector that feels loose.",
            ],
        },
    },
}
