FLOW = {
    "title": "Docking Issues",
    "start": "q_multiple_robots",
    "nodes": {

        # ── PHASE 1: ISOLATE ROBOT VS STATION ────────────────────────────────

        "q_multiple_robots": {
            "type": "question",
            "text": "Does the docking failure happen with just ONE robot, or with ALL robots that try to dock to the same marker?",
            "hint": "This tells you if it's a robot problem or a docking station/marker problem.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Only one robot fails — others dock fine",            "next": "q_robot_errors",       "style": "warn"},
                {"label": "All robots fail at this marker",                     "next": "q_station_errors",     "style": "warn"},
                {"label": "Only one robot (can't test with others)",            "next": "q_robot_errors",       "style": "neutral"},
            ],
        },

        # ── ROBOT-SIDE ISSUES ─────────────────────────────────────────────────

        "q_robot_errors": {
            "type": "question",
            "text": "Does the robot report any error codes when the docking fails?",
            "hint": "Check the notification bell (top-right in the web interface) and the mission log for error codes.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — there is an error code",    "next": "sol_check_error_codes",    "style": "warn"},
                {"label": "No errors reported",              "next": "q_correct_map",             "style": "good"},
            ],
        },

        "q_correct_map": {
            "type": "question",
            "text": "Is the robot using the correct map — the one that has the docking marker on it?",
            "hint": "Go to Setup → Maps and confirm the map with the marker is shown as Active.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — correct map is active",        "next": "q_robot_can_reach_entry", "style": "good"},
                {"label": "No — wrong map or no active map",    "next": "sol_activate_map",        "style": "warn"},
            ],
        },

        "q_robot_can_reach_entry": {
            "type": "question",
            "text": "Can the robot physically reach the Entry position in front of the marker without hitting anything?",
            "hint": "Check if the robot's footprint or top module conflicts with nearby walls, racks, or the docking station itself.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — path to Entry position is clear", "next": "q_marker_detection",    "style": "good"},
                {"label": "No — path is blocked or too tight",     "next": "sol_blocked_path",       "style": "warn"},
            ],
        },

        "q_marker_detection": {
            "type": "question",
            "text": "Drive the robot manually to the marker's Entry position. In the web interface go to Monitoring → Safety System. Do the blue dots correctly represent the marker shape?",
            "hint": "Blue dots show what the laser scanners detect. For a V-marker you should see two lines in a V shape. Random or scattered dots = problem.",
            "info": (
                "What to look for:\n"
                "• Correct: blue dots clearly outline the marker shape (V, L, Bar, etc.)\n"
                "• Problem: many dots close to the robot → dirty/scratched scanners\n"
                "• Problem: scattered random dots → interference from lights or reflective surfaces\n"
                "• Problem: wrong shape → marker may be at wrong height\n\n"
                "Marker height requirements:\n"
                "• Deckload/hook robots: marker must be 200 mm from ground, at least 100 mm tall\n"
                "• Forklift robots: marker must be 140 mm from ground, at least 120 mm tall"
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — blue dots correctly show marker shape",  "next": "q_imu_calibrated",       "style": "good"},
                {"label": "Many dots close to robot (scanner issue)",      "next": "sol_clean_scanner_dock", "style": "warn"},
                {"label": "Scattered random dots (interference)",          "next": "sol_scanner_interference_dock", "style": "warn"},
                {"label": "Wrong shape detected",                          "next": "sol_marker_height",      "style": "warn"},
            ],
        },

        "q_imu_calibrated": {
            "type": "question",
            "text": "Has the robot had a USB restore, or had any of these parts replaced recently? (drive wheel, motor/bogie, encoder, power board, motor controller, robot computer, encoder cables)",
            "hint": "After any of these changes, the IMU must be recalibrated — otherwise docking accuracy is degraded.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — one of those parts was replaced or a USB restore was done", "next": "sol_imu_recalibrate", "style": "warn"},
                {"label": "No — nothing was changed",                                         "next": "q_fleet_resource",   "style": "good"},
            ],
        },

        "q_fleet_resource": {
            "type": "question",
            "text": "Is the robot connected to MiR Fleet? Does it stop and wait approximately 2 meters before the Entry position?",
            "hint": "In MiR Fleet, a robot waits 2m away if the marker/resource is already occupied by another robot.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — stops 2 m away and waits (Fleet resource occupied)",  "next": "sol_fleet_resource_occupied", "style": "warn"},
                {"label": "No — just fails to dock, no waiting behavior",              "next": "q_top_module_dock",          "style": "neutral"},
            ],
        },

        "q_top_module_dock": {
            "type": "question",
            "text": "Does the robot have a top module (shelf, pallet lift, hook, etc.)? Could the top module be causing scanner interference?",
            "hint": "Top modules with strong lights or that hang below the scanner line can interfere with marker detection.",
            "image": "assets/images/correct shelf carrier legs.jpeg",
            "video": None,
            "options": [
                {"label": "Yes — top module may be interfering",     "next": "sol_top_module_dock",   "style": "warn"},
                {"label": "No top module / not likely the cause",    "next": "sol_environment_dock",  "style": "neutral"},
            ],
        },

        # ── STATION/MARKER ISSUES ─────────────────────────────────────────────

        "q_station_errors": {
            "type": "question",
            "text": "Do robots report any error codes when they fail to dock at this marker?",
            "hint": "Check the mission log and notification bell for error codes when any robot tries to dock here.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — error codes are reported",    "next": "sol_check_error_codes",  "style": "warn"},
                {"label": "No error codes",                    "next": "q_map_quality",          "style": "neutral"},
            ],
        },

        "q_map_quality": {
            "type": "question",
            "text": "Is the map accurate around the docking marker area? Is it free of noise, gray holes, or stray black dots?",
            "hint": "A poor quality map affects docking precision. Zoom into the map around the marker in the web interface.",
            "image": "assets/images/scanner clean.jpeg",
            "video": None,
            "options": [
                {"label": "Yes — map looks clean and accurate",  "next": "q_marker_specs",      "style": "good"},
                {"label": "No — map is noisy or inaccurate",    "next": "sol_improve_map",      "style": "warn"},
            ],
        },

        "q_marker_specs": {
            "type": "question",
            "text": "Does the physical marker meet the specification requirements?",
            "hint": "Check height from floor, marker height, color, and that it matches the type selected in the robot interface.",
            "info": (
                "Marker requirements:\n"
                "• Deckload/hook robots: base 200 mm from ground, at least 100 mm tall\n"
                "• Forklift robots: base 140 mm from ground, at least 120 mm tall\n"
                "• Color: NOT reflective, transparent, pure white, or pure black\n"
                "• Recommended: matte iron gray (RAL 7011), max 10 GU gloss\n"
                "• Dimensions: must match the Relative Markers Drawing for the selected type\n\n"
                "In the robot interface: open the map → click the marker → Settings → verify the marker Type matches the physical shape."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — marker meets all specs",       "next": "q_marker_offsets",     "style": "good"},
                {"label": "No — marker does not meet specs",    "next": "sol_fix_marker",        "style": "warn"},
            ],
        },

        "q_marker_offsets": {
            "type": "question",
            "text": "Could the marker offsets be incorrect? Is the robot stopping in the wrong position relative to the marker?",
            "hint": "Marker offsets define where the robot positions itself relative to the marker center. You can re-detect the marker to recalibrate them.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — robot stops in wrong position",  "next": "sol_recalibrate_offsets",  "style": "warn"},
                {"label": "No — position looks correct",          "next": "sol_environment_dock",     "style": "neutral"},
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────────

        "sol_check_error_codes": {
            "type": "solution",
            "severity": "medium",
            "title": "Check Error Codes and Solutions",
            "image": None,
            "video": None,
            "steps": [
                "The robot is reporting an error code when docking fails.",
                "Go to the MiR Support Portal and find the document 'Error codes and solutions'.",
                "Look up the specific code shown in the robot's notification bell or mission log.",
                "Follow the recommended solution for that specific error code.",
                "If the error code is not found or the solution doesn't help, contact MiR Technical Support.",
            ],
        },

        "sol_activate_map": {
            "type": "solution",
            "severity": "easy",
            "title": "Wrong Map Active — Activate the Correct Map",
            "image": None,
            "video": None,
            "steps": [
                "The robot must be on the same map as the docking marker.",
                "In the robot interface, go to Setup → Maps.",
                "Find the map that contains the docking marker and activate it.",
                "After activating the map, re-localize the robot on that map.",
                "Try the docking mission again.",
            ],
        },

        "sol_blocked_path": {
            "type": "solution",
            "severity": "medium",
            "title": "Path to Entry Position Is Blocked or Too Narrow",
            "image": None,
            "video": None,
            "steps": [
                "The robot cannot reach the Entry position due to its footprint conflicting with obstacles or walls.",
                "Option 1: Adjust the robot's footprint in the robot interface to match its actual dimensions.",
                "Option 2: Move the Entry position to a location the robot can reach.",
                "Option 3: Adjust the docking offsets so the robot positions itself differently.",
                "Make sure the Entry position is at least 1–2 meters in front of the marker so the robot can align properly.",
                "Test the docking again after making adjustments.",
            ],
        },

        "sol_clean_scanner_dock": {
            "type": "solution",
            "severity": "easy",
            "title": "Dirty Laser Scanner Causing Poor Marker Detection",
            "image": "assets/images/scanner clean.jpeg",
            "video": None,
            "steps": [
                "The many blue dots close to the robot indicate dirty or scratched laser scanner lenses.",
                "Clean the laser scanner optics covers with a clean, dry, anti-static cloth.",
                "Check if the optics covers are scratched or physically damaged — if so, they must be replaced.",
                "After cleaning, drive the robot back to the Entry position and check the blue dots again.",
                "If cleaning resolves the issue, add scanner cleaning to your regular maintenance schedule.",
            ],
        },

        "sol_scanner_interference_dock": {
            "type": "solution",
            "severity": "medium",
            "title": "Scanner Interference Affecting Marker Detection",
            "image": None,
            "video": None,
            "steps": [
                "Random scattered blue dots indicate scanner interference from lights or reflective/transparent surfaces.",
                "Check the area around the marker for: direct lighting aimed at scanner level, shiny floors, glass walls, reflective shelves.",
                "Remove or shield the interfering source if possible.",
                "If interference cannot be removed, adjust the marker position or Entry position to avoid the affected zone.",
                "Transparent materials (like plastic curtains or glass panels) within 200 mm of the floor are common causes.",
            ],
        },

        "sol_marker_height": {
            "type": "solution",
            "severity": "medium",
            "title": "Marker at Wrong Height — Scanner Cannot Detect Correct Shape",
            "image": None,
            "video": None,
            "steps": [
                "The laser scanners are detecting a different shape than the marker — the marker is likely at the wrong height.",
                "Deckload/hook robots: marker base must be exactly 200 mm from the ground, and at least 100 mm tall.",
                "Forklift robots: marker base must be exactly 140 mm from the ground, and at least 120 mm tall.",
                "Adjust the marker height and test again by checking the blue dots in Monitoring → Safety System.",
            ],
        },

        "sol_imu_recalibrate": {
            "type": "solution",
            "severity": "medium",
            "title": "IMU Must Be Recalibrated After Part Replacement",
            "image": None,
            "video": None,
            "steps": [
                "After replacing drive wheels, motors/bogies, encoders, power board, motor controller, robot computer, or encoder cables — the IMU must be recalibrated.",
                "A USB restore also resets all calibrations.",
                "Without recalibration, the robot's dead reckoning is inaccurate, causing docking failures.",
                "Follow the guide 'How to calibrate the IMU' on the MiR Support Portal.",
                "After recalibration, test docking again.",
            ],
        },

        "sol_fleet_resource_occupied": {
            "type": "solution",
            "severity": "medium",
            "title": "Fleet: Marker Resource Is Occupied by Another Robot",
            "image": None,
            "video": None,
            "steps": [
                "The robot waits ~2 meters from the Entry position because the marker resource is occupied in MiR Fleet.",
                "This happens when a robot was manually pushed away from the resource without being assigned a mission to leave it.",
                "In the MiR Fleet interface, open the resource queue for the marker to see which robot is occupying it.",
                "Assign a new mission to the occupying robot to make it drive away and release the resource.",
                "The waiting robot should then proceed to dock.",
            ],
        },

        "sol_top_module_dock": {
            "type": "solution",
            "severity": "medium",
            "title": "Top Module Affecting Docking Performance",
            "image": None,
            "video": None,
            "steps": [
                "The top module may be affecting docking in one of these ways:",
                "• Emitting strong light that reflects into the laser scanners",
                "• Hanging load or attachment that extends into the scanner's field of view",
                "• Top module footprint collides with the marker or station structure",
                "Try removing the top module or its load and testing docking without it.",
                "If docking succeeds without the top module, adjust the top module design or docking offsets to compensate.",
                "Contact your top module manufacturer or MiR distributor for application-specific guidance.",
            ],
        },

        "sol_environment_dock": {
            "type": "solution",
            "severity": "medium",
            "title": "Check Time-of-Day / Environmental Changes",
            "image": None,
            "video": None,
            "steps": [
                "If docking fails at certain times of day but not others, the operating environment is changing.",
                "Common causes: sunlight moving through windows, shift changes causing different lighting, forklift traffic creating temporary obstacles.",
                "Note the exact times when docking fails and correlate with environmental changes.",
                "Add shielding or modify the docking approach to reduce environmental dependency.",
                "If the issue is unpredictable or cannot be isolated, contact MiR Technical Support with the robot serial number and a description of the failure pattern.",
            ],
        },

        "sol_improve_map": {
            "type": "solution",
            "severity": "medium",
            "title": "Poor Map Quality Around Marker — Clean the Map",
            "image": None,
            "video": None,
            "steps": [
                "The map quality around the docking marker is poor. This directly affects docking precision.",
                "In the robot interface, open the map editor and clean the area around the marker:",
                "• Remove noise (random black dots not representing real walls)",
                "• Fill in gray holes in the floor representation",
                "• Draw clean, complete wall lines",
                "• Mark areas the robot cannot drive through as Forbidden Zones",
                "After cleaning the map, re-localize the robot and test docking again.",
                "For a step-by-step guide, see the 'Map Cleaning' section in the MiR robot manual.",
            ],
        },

        "sol_fix_marker": {
            "type": "solution",
            "severity": "medium",
            "title": "Marker Does Not Meet Specifications",
            "image": None,
            "video": None,
            "steps": [
                "The physical marker does not meet MiR specifications — this causes unreliable or failed detection.",
                "Fix the marker to meet these requirements:",
                "• Deckload/hook: base 200 mm from ground, at least 100 mm tall",
                "• Forklift: base 140 mm from ground, at least 120 mm tall",
                "• Color: matte (max 10 GU gloss), ideally matte iron gray (RAL 7011)",
                "• Not white, black, reflective, or transparent",
                "• Dimensions must match the Relative Markers Drawing for the marker type (available on MiR Support Portal)",
                "After fixing the marker, also verify the correct marker type is selected in the robot interface (Setup → Maps → [marker] → Settings).",
            ],
        },

        "sol_recalibrate_offsets": {
            "type": "solution",
            "severity": "easy",
            "title": "Recalibrate Marker Offsets by Re-Detection",
            "image": None,
            "video": None,
            "steps": [
                "The marker offsets define where the robot stops relative to the marker center.",
                "To recalibrate: manually drive the robot to the exact desired docking position.",
                "In the robot interface, open the map → click the marker → Settings → select 'Detect'.",
                "The offsets will update to reflect the robot's current position.",
                "Test docking again after saving the new offsets.",
                "If the robot cannot reach the desired position, check for Forbidden Zones overlapping with the docked position.",
            ],
        },
    },
}
