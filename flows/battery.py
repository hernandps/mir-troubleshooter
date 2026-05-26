FLOW = {
    "title": "Battery Issues",
    "start": "q_battery_symptom",
    "nodes": {

        # ── PHASE 1: IDENTIFY SYMPTOM ─────────────────────────────────────────

        "q_battery_symptom": {
            "type": "question",
            "text": "What is the battery symptom you are seeing?",
            "hint": "Select the closest match to what is happening with your robot.",
            "info": (
                "Common battery symptoms:\n"
                "• Power button doesn't light at all → no power from battery\n"
                "• Power button lights red → battery critically low\n"
                "• Stop button flashes every ~15 seconds → battery in Power Save mode\n"
                "• Power/Stop button flickers when charger connected → battery issue while charging\n"
                "• Battery won't charge (charger doesn't hum or LED stays wrong color)"
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Power button doesn't light / robot won't turn on",   "next": "q_can_bus_voltage",    "style": "warn"},
                {"label": "Power button red or Stop button flashing ~15s",       "next": "q_can_bus_voltage",    "style": "warn"},
                {"label": "Battery won't charge (charger connected but no charging)", "next": "q_can_bus_voltage", "style": "warn"},
                {"label": "Button flickers when charger connected",              "next": "q_dual_charging",      "style": "warn"},
            ],
        },

        # ── DUAL CHARGING CHECK ───────────────────────────────────────────────

        "q_dual_charging": {
            "type": "question",
            "text": "Was the robot connected to BOTH a cable charger AND a charging station at the same time when it shut down?",
            "hint": "MiR250 only: connecting both simultaneously can cause an over-current condition that shuts down the battery.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — both charger and charging station were connected",  "next": "sol_dual_charging",  "style": "warn"},
                {"label": "No — only one was connected",                             "next": "q_can_bus_voltage",  "style": "good"},
            ],
        },

        # ── PHASE 2: CAN BUS VOLTAGE CHECK ────────────────────────────────────

        "q_can_bus_voltage": {
            "type": "checklist",
            "text": "Measure the CAN bus voltage on the battery",
            "hint": "This tells you if the battery's internal BMS (Battery Management System) is still active.",
            "info": (
                "You will need a multimeter. This check requires removing the battery from the robot.\n\n"
                "Steps:\n"
                "1. Turn off the robot and remove the battery from the robot.\n"
                "2. Make sure the battery is NOT connected to a charger.\n"
                "3. Locate the battery connector pins: CAN High (or CAN Low) and Power - (minus).\n"
                "4. Place one probe on CAN High (or CAN Low) and the other on Power - (minus).\n"
                "5. Read the voltage.\n\n"
                "Expected: ~3 V if the CAN bus is active.\n"
                "If below 2.5 V → BMS is inactive (deep sleep or defective)."
            ),
            "image": "assets/images/Moc Cable.jpeg",
            "video": None,
            "items": [
                {
                    "key": "battery_removed",
                    "label": "Battery removed from robot and disconnected from all chargers.",
                },
                {
                    "key": "voltage_measured",
                    "label": "Measured voltage from CAN High (or CAN Low) pin to Power - (minus) pin.",
                },
            ],
            "options": [
                {
                    "label": "CAN voltage is above 2.5 V — BMS active",
                    "next": "q_host_voltage",
                    "style": "good",
                    "requires": ["battery_removed", "voltage_measured"],
                },
                {
                    "label": "CAN voltage is below 2.5 V — BMS inactive",
                    "next": "q_deep_sleep_charger",
                    "style": "warn",
                },
            ],
        },

        # ── PATH: CAN BUS INACTIVE (< 2.5 V) ─────────────────────────────────

        "q_deep_sleep_charger": {
            "type": "question",
            "text": "CAN bus is inactive (battery may be in Deep Sleep). Do you have a MiR Cable Charger Lite 48V 3A (the small cable charger)?",
            "hint": "The 3A cable charger is the only charger that can recover a battery in Deep Sleep. The 20A charger will NOT recover it.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — I have the 3A cable charger",  "next": "q_charge_6h_result",   "style": "good"},
                {"label": "No — I only have a 20A or other charger", "next": "sol_no_3a_charger", "style": "warn"},
            ],
        },

        "q_charge_6h_result": {
            "type": "question",
            "text": "Connect the 3A charger directly to the battery using the adapter cable. Charge for 6–8 hours. After charging, measure the CAN bus voltage again. Is it now above 2.5 V?",
            "hint": "Connect adapter cable to battery first, then connect the charger. Let it charge for the full 6–8 hours.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — CAN voltage now above 2.5 V (battery recovered)", "next": "sol_deep_sleep_recovered", "style": "good"},
                {"label": "No — still below 2.5 V after 6–8 hours",               "next": "sol_battery_defective",    "style": "warn"},
            ],
        },

        # ── PATH: CAN BUS ACTIVE (> 2.5 V) — MEASURE HOST VOLTAGE ────────────

        "q_host_voltage": {
            "type": "question",
            "text": "Measure the HOST voltage of the battery and apply the correction factor. What is the corrected host voltage?",
            "hint": "Use a high-quality multimeter. Measure from Host-detect pin to Power - (minus) pin. The internal 1 MΩ resistor affects readings — multiply your reading by (meter resistance + 1) / meter resistance.",
            "info": (
                "The Host-detect pin has a 1 MΩ internal resistor (voltage divider effect).\n\n"
                "Correction formula:  Actual V = Measured V × (meter_Ω + 1 MΩ) / meter_Ω\n"
                "Example: If your multimeter has 10 MΩ resistance and reads 29.3 V:\n"
                "  Actual = 29.3 × (10+1)/10 = 32.2 V\n\n"
                "You can find your multimeter's input impedance in its datasheet, or measure it with another meter.\n"
                "A standard quality multimeter is typically 10 MΩ.\n\n"
                "⚠️ Take a photo of the voltage reading and probe setup — needed if you contact support."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Above ~36–42 V (Low power or Operable mode)",  "next": "q_operable_charging",   "style": "good"},
                {"label": "32.5 V to ~36–42 V (Power Save mode)",         "next": "q_power_save_charge",   "style": "warn"},
                {"label": "26–32.5 V (Deep Sleep mode)",                   "next": "q_deep_sleep_charger",  "style": "warn"},
                {"label": "3–26 V (Shut down / unrecoverable)",            "next": "sol_battery_shutdown",  "style": "warn"},
            ],
        },

        # ── OPERABLE/LOW POWER MODE ────────────────────────────────────────────

        "q_operable_charging": {
            "type": "question",
            "text": "Battery appears to be in Operable or Low Power mode. Connect the 3A charger directly. Does the charger charge the battery?",
            "hint": "The charger should hum and its indicator LED should show charging activity.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — charger is charging the battery",     "next": "sol_charge_robot_check",  "style": "good"},
                {"label": "No — charger won't charge despite good voltage", "next": "q_discharge_voltage", "style": "warn"},
            ],
        },

        "q_discharge_voltage": {
            "type": "question",
            "text": "With the charger disconnected, measure the voltage between the + and – terminals on the battery adapter cable. Is the voltage close to the battery's calculated voltage (not near 0 V)?",
            "hint": "Do NOT apply a correction factor for this measurement. This checks if the battery can discharge.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — voltage is close to calculated value (battery CAN discharge)",  "next": "sol_cannot_charge_can_discharge",   "style": "warn"},
                {"label": "No — voltage is near 0 V (battery cannot discharge either)",          "next": "sol_cannot_charge_or_discharge",    "style": "warn"},
            ],
        },

        # ── POWER SAVE MODE ────────────────────────────────────────────────────

        "q_power_save_charge": {
            "type": "question",
            "text": "Battery is in Power Save mode (fully discharged). Charge directly with the 3A charger for at least 6–8 hours. After charging, does the robot turn on?",
            "hint": "Power Save mode occurs when the battery is stored too long or the Manual Brake Release switch was left ON. The 3A charger is required.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — robot now turns on after charging",          "next": "sol_power_save_recovered",  "style": "good"},
                {"label": "No — still won't turn on after 6–8 hours charging", "next": "q_can_voltage_after_charge", "style": "warn"},
            ],
        },

        "q_can_voltage_after_charge": {
            "type": "question",
            "text": "Measure the CAN bus voltage again after the charge attempt. Is it above 2.5 V?",
            "hint": "Same measurement as before: CAN High or CAN Low pin to Power - (minus).",
            "image": None,
            "video": None,
            "options": [
                {"label": "CAN voltage now above 2.5 V",  "next": "sol_power_save_support",  "style": "warn"},
                {"label": "CAN voltage still below 2.5 V", "next": "sol_battery_defective",  "style": "warn"},
            ],
        },

        # ── CHECK ROBOT SIDE ──────────────────────────────────────────────────

        "q_check_robot_side": {
            "type": "checklist",
            "text": "Check the robot's inrush circuit (power board capacitance)",
            "hint": "A faulty power board can damage the battery with high inrush current. This test verifies the power board.",
            "info": (
                "⚠️ Robot must be OFF and battery disconnected for this test.\n\n"
                "Steps:\n"
                "1. Disconnect all cable chargers and charging stations.\n"
                "2. Turn off robot, disconnect battery, and remove it.\n"
                "3. Wait at least 5 minutes for capacitors to fully discharge.\n"
                "4. Using a multimeter capable of measuring capacitance up to 5000 μF,\n"
                "   measure capacitance between + and - pins on the battery cable connector.\n"
                "   (+ pin = red cable, - pin = black cable)\n\n"
                "Expected: below 100 μF (normal is ~100 nF)\n"
                "⚠️ If you read 2000–2500 μF → power board is faulty and must NOT be connected to battery again."
            ),
            "image": None,
            "video": None,
            "items": [
                {"key": "robot_off", "label": "Robot is OFF, battery disconnected, all chargers disconnected."},
                {"key": "waited_5min", "label": "Waited at least 5 minutes for capacitors to discharge."},
                {"key": "measured_cap", "label": "Measured capacitance between + and - pins on the battery cable connector."},
            ],
            "options": [
                {
                    "label": "Reading below 100 μF — power board is OK",
                    "next": "sol_battery_replace",
                    "style": "good",
                    "requires": ["robot_off", "waited_5min", "measured_cap"],
                },
                {
                    "label": "Reading is 2000–2500 μF — power board is FAULTY",
                    "next": "sol_power_board_faulty",
                    "style": "warn",
                },
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────────

        "sol_dual_charging": {
            "type": "solution",
            "severity": "hard",
            "title": "Over-Current from Simultaneous Charging (MiR250)",
            "image": None,
            "video": None,
            "steps": [
                "The robot was connected to both a cable charger and a charging station at the same time.",
                "This causes an over-current condition that can shut down the battery.",
                "NEVER connect both simultaneously on MiR250.",
                "Contact MiR Technical Support and inform them: 'Battery has shut down due to over-current while charging on MiR250.'",
                "Have ready: robot serial number, date the battery shut down, and confirmation of dual-charger connection.",
            ],
        },

        "sol_no_3a_charger": {
            "type": "solution",
            "severity": "hard",
            "title": "Deep Sleep — 3A Charger Required",
            "image": None,
            "video": None,
            "steps": [
                "The battery is in Deep Sleep (CAN bus below 2.5 V) and can only be recovered with the MiR Cable Charger Lite 48V 3A.",
                "The 20A charger or other chargers will NOT recover a battery in Deep Sleep.",
                "Contact MiR Technical Support and inform them: 'Battery has entered Deep Sleep (HW shutdown) and I don't have a MiR Cable Charger Lite 48V 3A.'",
                "Include: robot serial number, photo of the CAN bus voltage measurement.",
                "Order a MiR Cable Charger Lite 48V 3A (order number: contact your distributor).",
            ],
        },

        "sol_deep_sleep_recovered": {
            "type": "solution",
            "severity": "easy",
            "title": "Battery Recovered from Deep Sleep",
            "image": None,
            "video": None,
            "steps": [
                "The battery was in Deep Sleep but has been recovered by the 3A charger.",
                "Reconnect the battery to the robot and try turning it on.",
                "Let the battery charge to a healthy level before returning to normal operations.",
                "To prevent recurrence: do not leave the robot stored for more than 3 months without charging.",
                "Also check: was the Manual Brake Release switch left in the ON position? That drains the battery faster.",
            ],
        },

        "sol_battery_defective": {
            "type": "solution",
            "severity": "hard",
            "title": "Battery Is Defective or Unrecoverable",
            "image": None,
            "video": None,
            "steps": [
                "The battery's CAN bus voltage remains below 2.5 V even after 6–8 hours of charging with the 3A charger.",
                "This indicates the battery is defective or has been in Deep Sleep for too long (over 60 days at 0%).",
                "Before contacting support, also check the robot's power board — a faulty power board can damage batteries.",
                "Take a photo of the CAN bus voltage measurement and probe setup.",
                "Contact MiR Technical Support with: robot serial number, photo of measurement, and write: 'Battery is not in Deep Sleep (HW shutdown), and the CAN high/low voltage is less than 2.5 V.'",
                "The battery likely needs replacement.",
            ],
        },

        "sol_charge_robot_check": {
            "type": "solution",
            "severity": "easy",
            "title": "Battery Is Charging — Check Robot Side Too",
            "image": None,
            "video": None,
            "steps": [
                "The battery is charging correctly.",
                "Let it charge for 1–2 hours.",
                "While charging, also check the robot's internal power circuit to rule out a robot-side cause:",
                "→ Check if any top module draws excessive current (see Hardware Health → Power Supply → TOP_FUSE).",
                "→ Verify no custom non-MiR chargers have been used.",
                "→ If you recently replaced a part (power board, motor controller), verify cables are correctly connected.",
                "After charging, reconnect the battery to the robot and test normal operation.",
            ],
        },

        "sol_cannot_charge_can_discharge": {
            "type": "solution",
            "severity": "hard",
            "title": "Battery Can Discharge but Cannot Charge",
            "image": None,
            "video": None,
            "steps": [
                "The battery can discharge (voltage present at adapter) but will not accept a charge.",
                "Take a photo of the voltage reading and probe setup.",
                "Contact MiR Technical Support with: robot serial number, photo, and write:",
                "'The battery cannot charge but it can discharge, and the measured voltage over the adapter is [your voltage reading].'",
                "Also check the robot's power circuit before sending the request — a faulty power board can cause this.",
            ],
        },

        "sol_cannot_charge_or_discharge": {
            "type": "solution",
            "severity": "hard",
            "title": "Battery Cannot Charge or Discharge",
            "image": None,
            "video": None,
            "steps": [
                "The battery cannot charge or discharge — it is in a failed state.",
                "Take a photo of the adapter voltage reading (near 0 V) and the host voltage measurement.",
                "Contact MiR Technical Support with: robot serial number, both photos, and write:",
                "'The battery cannot charge or discharge, and the calculated host voltage is [your corrected value].'",
                "Also check the robot's power board for high inrush current (capacitance test) — see the 'Check robot inrush circuit' flow.",
            ],
        },

        "sol_power_save_recovered": {
            "type": "solution",
            "severity": "easy",
            "title": "Battery Recovered from Power Save Mode",
            "image": None,
            "video": None,
            "steps": [
                "The battery was in Power Save mode (fully discharged) and has been recovered by direct charging.",
                "To prevent recurrence:",
                "• Do not store the robot for extended periods without keeping the battery charged.",
                "• Check that the Manual Brake Release switch is always in the OFF position when not in use.",
                "• The brake release switch left ON drains the battery continuously and can cause Power Save mode.",
                "Resume normal operations. Monitor battery percentage regularly.",
            ],
        },

        "sol_power_save_support": {
            "type": "solution",
            "severity": "hard",
            "title": "Battery in Power Save — CAN Active but Still Not Working",
            "image": None,
            "video": None,
            "steps": [
                "After charging, the CAN bus is active (above 2.5 V) but the battery still won't power the robot.",
                "Contact MiR Technical Support with: robot serial number and write:",
                "'The battery cannot charge or discharge, but the host voltage is [calculated value], and the CAN high/low voltage is above 2.5 V.'",
                "Also check the robot's power board (inrush current test) before sending the support request.",
            ],
        },

        "sol_battery_shutdown": {
            "type": "solution",
            "severity": "hard",
            "title": "Battery in Shutdown / Unrecoverable State",
            "image": None,
            "video": None,
            "steps": [
                "The host voltage is between 3–26 V — the battery is over-discharged and in a shutdown state.",
                "Common causes: battery stored in Deep Sleep for more than 60 days, physical damage from impact, or a faulty robot power board.",
                "First check the robot's power board for high inrush current before assuming the battery is to blame.",
                "Contact MiR Technical Support with: robot serial number, photo of host voltage measurement, and write:",
                "'The host voltage is [value] V and the battery appears to be in shutdown state.'",
                "The battery likely needs replacement.",
            ],
        },

        "sol_battery_replace": {
            "type": "solution",
            "severity": "hard",
            "title": "Power Board OK — Battery Needs Replacement",
            "image": None,
            "video": None,
            "steps": [
                "The power board inrush current is normal (capacitance below 100 μF).",
                "The battery itself is the faulty component.",
                "Contact MiR Technical Support or your MiR distributor to order a replacement battery.",
                "Have ready: robot serial number, battery serial number (on the battery label), and the fault description.",
            ],
        },

        "sol_power_board_faulty": {
            "type": "solution",
            "severity": "hard",
            "title": "Power Board Is Faulty — Do NOT Connect Battery",
            "image": None,
            "video": None,
            "steps": [
                "⚠️ CRITICAL: The power board capacitance measured 2000–2500 μF — the power board is faulty.",
                "Do NOT reconnect the battery to this robot until the power board is replaced.",
                "A faulty power board will damage any battery connected to it.",
                "If the battery was connected to this power board for an extended time, it may already be unusable.",
                "Contact MiR Technical Support immediately.",
                "Have ready: robot serial number, capacitance reading, and confirmation that the battery was connected to this power board.",
            ],
        },
    },
}
