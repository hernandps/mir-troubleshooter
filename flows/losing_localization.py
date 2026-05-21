FLOW = {
    "title": "Robot Losing Localization",
    "start": "q_localization_symptom",
    "nodes": {

        # ── PHASE 1: IDENTIFY SYMPTOM ─────────────────────────────────────────

        "q_localization_symptom": {
            "type": "question",
            "text": "What localization problem are you seeing?",
            "hint": "Localization = the robot knowing where it is on the map.",
            "info": (
                "In the web interface, the robot's position on the map is shown by the robot icon.\n"
                "If localization is wrong, the icon will not match the robot's real position.\n\n"
                "Tip: Open Monitoring → Safety system to see the live laser scanner view (red dots = detected obstacles). "
                "If the dots don't match the real environment, the scanner may be the issue."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Robot drifts or teleports on the map",        "next": "q_scanner_clean",    "style": "neutral"},
                {"label": "'Localization lost' error in web interface",  "next": "q_scanner_clean",    "style": "warn"},
                {"label": "Robot drives to wrong positions/misses goals", "next": "q_map_quality",     "style": "neutral"},
            ],
        },

        # ── PHASE 2: SCANNERS AND WHEELS ─────────────────────────────────────

        "q_scanner_clean": {
            "type": "checklist",
            "text": "Check and clean the safety laser scanners and wheels",
            "hint": "Dirty or scratched scanners give inaccurate distance data, which causes localization errors. Slipping wheels also cause drift.",
            "image": "assets/images/scanner clean.jpeg",
            "video": None,
            "info": (
                "The robot uses laser scanner data to compare against the map and find its position. "
                "If scanners are dirty or damaged, the data is wrong and localization fails.\n\n"
                "The wheels also matter — if a wheel slips or has flat spots, the robot's internal position estimate drifts "
                "even before the scanner can correct it."
            ),
            "items": [
                {
                    "key": "scanner_clean",
                    "label": "Cleaned both safety laser scanner lenses with a clean anti-static cloth — no scratches or cracks visible.",
                },
                {
                    "key": "wheels_clean",
                    "label": "Checked all wheels: clean, not wrapped with debris, and rotate freely when the robot is lifted.",
                },
                {
                    "key": "wheels_not_worn",
                    "label": "Wheels are not worn down (no flat spots, no significant rubber loss). Heavily worn wheels must be replaced.",
                },
            ],
            "options": [
                {
                    "label": "Found an issue (dirty scanner or worn wheel) — fixed it",
                    "next": "sol_scanner_wheel_fixed",
                    "style": "good",
                },
                {
                    "label": "Everything looks OK — continue to map quality check",
                    "next": "q_map_quality",
                    "style": "neutral",
                    "requires": ["scanner_clean", "wheels_clean", "wheels_not_worn"],
                },
            ],
        },

        # ── PHASE 3: MAP QUALITY ──────────────────────────────────────────────

        "q_map_quality": {
            "type": "question",
            "text": "How is the quality of the map the robot is using?",
            "hint": "Go to Setup → Maps in the web interface and inspect the active map carefully.",
            "info": (
                "A good localization map should have:\n"
                "• Clear, clean outlines of walls and permanent structures\n"
                "• No gray patches or holes in floor areas\n"
                "• No black outlier data points floating in open space\n"
                "• No obstacles that have since been removed from the real environment\n\n"
                "A poor map is one of the most common causes of localization problems."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Map looks clean and accurate",           "next": "q_unique_landmarks", "style": "good"},
                {"label": "Map has gray patches, holes, or noise",  "next": "sol_improve_map",    "style": "warn"},
                {"label": "Map has obstacles that no longer exist", "next": "sol_improve_map",    "style": "warn"},
            ],
        },

        # ── PHASE 4: LANDMARKS ────────────────────────────────────────────────

        "q_unique_landmarks": {
            "type": "question",
            "text": "Does the robot's operating area have unique recognizable features the robot can use to localize?",
            "hint": "Long featureless corridors or large open rooms make localization unreliable. Machines, pillars, or equipment corners help.",
            "info": (
                "The robot matches what its scanners currently see to the map to determine its position. "
                "If the environment is too uniform or symmetrical, there is nothing distinctive to match against.\n\n"
                "Good landmark examples:\n"
                "• Machines, equipment, and shelving units visible at scanner height\n"
                "• Corners, pillars, or distinctive wall shapes\n\n"
                "Poor environments for localization:\n"
                "• Long corridors with featureless parallel walls\n"
                "• Large open warehouses\n"
                "• Areas where the layout changes frequently"
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — area has distinct permanent landmarks",              "next": "q_encoder_test", "style": "good"},
                {"label": "No — area is open, symmetrical, or featureless",           "next": "sol_add_landmarks", "style": "warn"},
                {"label": "Environment changes frequently (moved equipment, doors)",  "next": "sol_dynamic_env",   "style": "warn"},
            ],
        },

        # ── PHASE 5: ENCODER / DRIVE CHECK ───────────────────────────────────

        "q_encoder_test": {
            "type": "question",
            "text": "Does the robot drive in a straight line when commanded to go straight?",
            "hint": "Drive the robot manually in a long straight line and observe if it curves to one side.",
            "info": (
                "A robot that consistently pulls to one side has a wheel encoder or drive imbalance. "
                "This causes the robot's internal position estimate to drift, making localization harder.\n\n"
                "To run a formal encoder test:\n"
                "• In some software versions: System → Diagnostics → Encoder test\n"
                "• Or drive manually and observe behavior"
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — robot drives straight",          "next": "sol_escalate_localization", "style": "good"},
                {"label": "No — robot curves or pulls to one side", "next": "sol_encoder_issue",       "style": "warn"},
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────────

        "sol_scanner_wheel_fixed": {
            "type": "solution",
            "severity": "easy",
            "title": "Scanner or Wheel Issue Resolved",
            "image": None,
            "video": None,
            "steps": [
                "After cleaning the scanner or addressing wheel wear, manually re-localize the robot on the map.",
                "In the web interface: drag the robot icon to the correct position on the map, or use the manual localization tool.",
                "Drive the robot or run a mission to verify that localization holds during operation.",
                "Schedule regular scanner lens cleaning and wheel inspections as part of preventive maintenance.",
                "If localization still drifts after the fix, check map quality next.",
            ],
        },

        "sol_improve_map": {
            "type": "solution",
            "severity": "medium",
            "title": "Map Quality Needs Improvement",
            "image": None,
            "video": None,
            "steps": [
                "A poor-quality map is one of the most common causes of localization failures.",
                "Options to improve the map:",
                "• **Remap the area**: drive the robot slowly and carefully through the full environment to create a new clean map.",
                "• **Edit the existing map**: use the map editor to remove ghost obstacles, fill gray patches, and clean up noise.",
                "• Ensure the map only contains **permanent structures** — not temporary objects (pallets, carts, people).",
                "After improving the map, re-localize the robot and test navigation on a full mission.",
                "If the map has been updated recently and the problem started then, roll back to the previous map.",
            ],
        },

        "sol_add_landmarks": {
            "type": "solution",
            "severity": "medium",
            "title": "Add Landmarks to Improve Localization",
            "image": None,
            "video": None,
            "steps": [
                "The operating area does not have enough unique features for reliable laser-based localization.",
                "Solutions:",
                "• **Add physical landmarks**: place distinctive objects — MiR reflector markers, equipment, or structures — at scanner height in featureless areas.",
                "• **Remap after adding landmarks**: create a new map with the new landmarks included.",
                "• **Split large maps**: if the area is very large and uniform, consider using smaller map zones.",
                "Contact MiR Technical Support or your distributor for guidance on challenging localization environments.",
            ],
        },

        "sol_dynamic_env": {
            "type": "solution",
            "severity": "medium",
            "title": "Dynamic Environment Affecting Localization",
            "image": None,
            "video": None,
            "steps": [
                "The environment changes frequently — moved equipment, doors, or temporary objects affect localization.",
                "Ensure the map only reflects the **permanent structure** of the environment (walls, fixed machinery).",
                "Do not map temporary objects (pallets, carts, parked vehicles) into the map.",
                "If doors along the route are sometimes open and sometimes closed, map them as open (worst case scenario for the scanner).",
                "Configure the robot's forbidden zones and virtual walls to match the current layout.",
                "Contact MiR Technical Support if localization fails consistently in a specific area.",
            ],
        },

        "sol_encoder_issue": {
            "type": "solution",
            "severity": "hard",
            "title": "Drive Imbalance — Encoder or Bogey Issue",
            "image": "assets/images/oil bogie.jpeg",
            "video": None,
            "steps": [
                "The robot pulls to one side when driving straight — this indicates a drive imbalance.",
                "Check both drive bogeys for:",
                "• Oil leaks or visible mechanical damage (see photo above).",
                "• Wheels that are significantly more worn on one side than the other.",
                "• One bogey that feels stiffer or harder to turn by hand (with brakes released manually).",
                "If the imbalance is severe, the bogey or motor controller may need inspection or replacement.",
                "Contact technical support with: robot serial number and a description of which side the robot pulls toward.",
            ],
        },

        "sol_escalate_localization": {
            "type": "solution",
            "severity": "hard",
            "title": "Localization Still Failing — Escalate to Support",
            "image": None,
            "video": None,
            "steps": [
                "Scanners are clean, wheels are good, map quality is good, landmarks are present, and drive is straight — but localization still fails.",
                "Collect diagnostic information:",
                "• Export the error log: System → Error Log → Export.",
                "• Generate a SICK report: System → SICK Report.",
                "• Take a screenshot of the map view when the localization loss occurs.",
                "• Note the exact conditions when it fails (specific location, time of day, load on robot, etc.).",
                "Contact MiR Technical Support with: robot serial number, error log, SICK report, and screenshots.",
            ],
        },
    },
}
