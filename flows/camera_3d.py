FLOW = {
    "title": "3D Camera Issues",
    "start": "q_camera_symptom",
    "nodes": {

        # ── PHASE 1: SYMPTOM ──────────────────────────────────────────────────

        "q_camera_symptom": {
            "type": "question",
            "text": "What is the 3D camera issue you are seeing?",
            "hint": "Check Monitoring → System Log for camera-related error messages.",
            "info": (
                "In Monitoring → System Log, look for:\n"
                "• 'OpCodes do not match! Sent X but received Y!' → camera firmware issue\n"
                "• 'Resetting camera device...' → software update needed\n"
                "• Poor connection / missing data errors → cable issue\n"
                "• Robot detecting non-existent obstacles or missing real ones → calibration or filter issue"
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "'OpCodes do not match' error in System Log",         "next": "sol_update_camera_fw",    "style": "warn"},
                {"label": "'Resetting camera device...' in System Log",         "next": "sol_update_robot_sw",     "style": "warn"},
                {"label": "Poor connection / missing data errors in System Log", "next": "q_camera_cable",         "style": "warn"},
                {"label": "Robot detects non-existent obstacles / misses real obstacles", "next": "q_laser_correct", "style": "warn"},
            ],
        },

        # ── PATH: CONNECTION / CABLE ISSUES ───────────────────────────────────

        "q_camera_cable": {
            "type": "question",
            "text": "Inspect the USB cables connecting the 3D cameras to the robot computer. Try replacing them with a USB 3.0 data cable. Does the camera connect after the cable swap?",
            "hint": "⚠️ The replacement cable MUST be USB 3.0 and capable of data transfer — a charging-only USB cable will NOT work.",
            "info": (
                "Access the camera USB cables:\n"
                "• MiR250: remove the front cover to access the cameras\n"
                "• MiR600/1350: open the front electronics drawer\n\n"
                "Disconnect the USB cable from the camera, replace with a known-good USB 3.0 data cable.\n"
                "Robot does NOT need to be powered for this check — turn off and disconnect battery before opening covers."
            ),
            "image": "assets/images/removed front cover.jpeg",
            "video": None,
            "options": [
                {"label": "Yes — camera connects with new USB 3.0 cable",  "next": "sol_replace_usb_cable",  "style": "good"},
                {"label": "No — still no connection with new cable",       "next": "q_direct_pc_connect",    "style": "warn"},
            ],
        },

        "q_direct_pc_connect": {
            "type": "question",
            "text": "Try connecting the camera directly to your PC with a USB 3.0 cable. Can your PC detect the camera using the Intel RealSense Viewer or Dynamic Calibrator tool?",
            "hint": "Use a Windows 10 PC with a USB 3.0 port (marked with 'SS' symbol). PC must be on Windows RS2 1706 or higher with updated drivers.",
            "info": (
                "Download Intel® RealSense™ Dynamic Calibrator:\n"
                "https://downloadcenter.intel.com/download/28517/Intel-RealSense-D400-Series-Calibration-Tools-and-API\n\n"
                "Steps:\n"
                "MiR250: remove front cover → disconnect camera USB → connect to PC via USB 3.0\n"
                "MiR600/1350: open electronics drawer → disconnect camera USB from robot computer → connect to PC\n\n"
                "Verify the USB port on your PC has the 'SS' (SuperSpeed) symbol."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — PC can detect the camera",      "next": "sol_factory_reset_camera",  "style": "good"},
                {"label": "No — camera not detected by PC either", "next": "sol_replace_camera",      "style": "warn"},
            ],
        },

        # ── PATH: DETECTION ISSUES ─────────────────────────────────────────────

        "q_laser_correct": {
            "type": "question",
            "text": "In the robot's active map view, do the red lines correctly represent real walls and obstacles around the robot?",
            "hint": "Red lines = what the safety laser scanners detect at 200 mm from the ground. If these are wrong, the laser scanners are the issue, not the 3D cameras.",
            "info": (
                "On the active map:\n"
                "• Red lines = safety laser scanner data (200 mm from ground)\n"
                "• Blue/purple obstacle clouds = combined data from lasers + 3D cameras (only visible when robot is moving)\n\n"
                "If the red lines are wrong → laser scanner issue, not camera issue\n"
                "If the red lines are correct but obstacle clouds are wrong → camera calibration or filter issue"
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "No — red lines are wrong (laser scanner issue)",    "next": "sol_laser_not_camera",  "style": "warn"},
                {"label": "Yes — red lines are correct (camera is the issue)", "next": "q_camera_environment",  "style": "good"},
            ],
        },

        "q_camera_environment": {
            "type": "question",
            "text": "Does the area where the camera detects phantom obstacles contain any of these: transparent objects, reflective surfaces, structures with repetitive patterns, or strong direct lighting?",
            "hint": "3D cameras using structured light or stereo vision are sensitive to these environmental factors.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — one of those conditions is present",   "next": "q_camera_filter",     "style": "warn"},
                {"label": "No — environment appears normal",            "next": "q_camera_filter",     "style": "neutral"},
            ],
        },

        "q_camera_filter": {
            "type": "question",
            "text": "Have you tried adjusting the camera filter settings in System → Settings → 3D Cameras?",
            "hint": "You can make cameras more or less sensitive to obstacles by changing filter, threshold, and depth preset settings.",
            "info": (
                "How to adjust camera filter settings:\n"
                "1. Position the robot in the area where phantom obstacles appear\n"
                "2. Confirm on the map that obstacle clouds appear where no obstacles exist\n"
                "3. Go to System → Settings → 3D Cameras\n"
                "4. Adjust the settings for the camera causing the issue\n"
                "5. Select 'Save changes'\n"
                "6. Check the map to see if phantom clouds have disappeared\n\n"
                "⚠️ Changing these settings affects the robot's obstacle detection behavior.\n"
                "Always test the robot's full driving behavior after making changes."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — adjusted filters but phantom obstacles remain", "next": "q_camera_contamination", "style": "warn"},
                {"label": "No — haven't tried adjusting filters yet",            "next": "sol_adjust_filters",    "style": "neutral"},
            ],
        },

        "q_camera_contamination": {
            "type": "question",
            "text": "Even at maximum filter settings the phantom obstacles remain. Are the camera lenses visibly dirty, scratched, or damaged?",
            "hint": "Clean the 3D cameras with a clean anti-static cloth. Look for scratches on the camera glass.",
            "image": "assets/images/crashed camera.jpeg",
            "video": None,
            "options": [
                {"label": "Yes — cameras are dirty, scratched, or damaged",  "next": "sol_camera_damage",       "style": "warn"},
                {"label": "No — cameras look clean and undamaged",           "next": "sol_recalibrate_camera",  "style": "neutral"},
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────────

        "sol_update_camera_fw": {
            "type": "solution",
            "severity": "medium",
            "title": "Update Camera Firmware",
            "image": None,
            "video": None,
            "steps": [
                "The 'OpCodes do not match' error indicates a camera firmware version mismatch.",
                "The easiest fix is to update the robot software to version 2.8.0 or higher.",
                "With version 2.8.0+, the camera firmware updates automatically during robot startup.",
                "Go to System → Software Update to check and update the robot software.",
                "If you need to update the camera firmware without updating the robot software, see the guide 'How to update the D435 3D camera firmware' on MiR Support Portal.",
                "After the update, restart the robot and verify the error is gone in System Log.",
            ],
        },

        "sol_update_robot_sw": {
            "type": "solution",
            "severity": "medium",
            "title": "Update Robot Software to Resolve Camera Reset Error",
            "image": None,
            "video": None,
            "steps": [
                "The 'Resetting camera device...' message in System Log indicates a known issue that was resolved in a later software version.",
                "Update the robot software: go to System → Software Update.",
                "Follow the update wizard to install the latest available version.",
                "After updating and restarting, monitor System Log to confirm the message no longer appears.",
            ],
        },

        "sol_replace_usb_cable": {
            "type": "solution",
            "severity": "easy",
            "title": "Faulty USB Cable — Replace It",
            "image": None,
            "video": None,
            "steps": [
                "The camera connected correctly after replacing the USB cable — the original cable was faulty.",
                "Replace the faulty USB cable with the new USB 3.0 data cable.",
                "Reassemble the robot, reconnect the battery, and restart.",
                "Verify the camera errors are gone in Monitoring → System Log.",
                "Keep a spare USB 3.0 cable on hand for future maintenance.",
            ],
        },

        "sol_factory_reset_camera": {
            "type": "solution",
            "severity": "medium",
            "title": "Factory Reset the Camera Using Intel Tool",
            "image": None,
            "video": None,
            "steps": [
                "The camera is detectable from a PC but has persistent issues — perform a factory reset.",
                "First, note the camera serial number: in the robot interface go to System → Settings → 3D Cameras.",
                "With the camera connected directly to your PC, open a Command Prompt and run:",
                "  Intel.Realsense.CustomRW -g -sn <camera_serial_number>",
                "If successful, you'll see: 'Calibration on device successfully reset to default gold factory settings.'",
                "Reconnect the camera to the robot computer, reassemble, reconnect battery, and restart.",
                "After restart, calibrate the camera using the guide 'How to calibrate a D435 3D camera' on MiR Support Portal.",
            ],
        },

        "sol_replace_camera": {
            "type": "solution",
            "severity": "hard",
            "title": "Camera Not Detected — Replace the 3D Camera",
            "image": "assets/images/crashed camera.jpeg",
            "video": None,
            "steps": [
                "The camera is not detected by either the robot or a PC — the camera hardware is faulty.",
                "The camera must be replaced.",
                "Contact MiR Technical Support or your distributor to order a replacement Intel RealSense D435 camera.",
                "Include: robot serial number, which camera is faulty (front/rear), and serial number from System → Settings → 3D Cameras.",
                "After replacement, calibrate the new camera: see 'How to calibrate a D435 3D camera' on MiR Support Portal.",
            ],
        },

        "sol_laser_not_camera": {
            "type": "solution",
            "severity": "medium",
            "title": "Issue Is With Laser Scanners, Not 3D Cameras",
            "image": None,
            "video": None,
            "steps": [
                "The red lines on the map are incorrect — the problem is with the safety laser scanners, not the 3D cameras.",
                "Go to the 'Constantly in Protective State' troubleshooting flow for laser scanner diagnosis.",
                "Common laser scanner issues: dirty lenses, reflective surfaces in the environment, cable faults, software needing update.",
            ],
        },

        "sol_adjust_filters": {
            "type": "solution",
            "severity": "medium",
            "title": "Adjust Camera Filter Settings",
            "image": None,
            "video": None,
            "steps": [
                "The 3D camera is detecting phantom obstacles — adjust the filter settings to reduce sensitivity.",
                "Position the robot where the phantom detection occurs.",
                "Go to System → Settings → 3D Cameras.",
                "Adjust the filter, threshold, and depth preset settings for the affected camera.",
                "Select 'Save changes' after each adjustment and check the map.",
                "Continue adjusting until the phantom obstacle clouds disappear.",
                "⚠️ Always test full robot driving behavior after changes — stronger filters may cause the robot to miss real obstacles.",
            ],
        },

        "sol_camera_damage": {
            "type": "solution",
            "severity": "hard",
            "title": "Camera Damaged or Severely Contaminated",
            "image": "assets/images/crashed camera.jpeg",
            "video": None,
            "steps": [
                "The camera lenses are scratched, cracked, or otherwise physically damaged.",
                "Scratched lenses cannot be cleaned — the camera must be replaced.",
                "Contact MiR Technical Support or your distributor for a replacement camera.",
                "If contaminated but not scratched: clean with an anti-static cloth and test again.",
                "After replacement: calibrate the new camera following the guide 'How to calibrate a D435 3D camera'.",
            ],
        },

        "sol_recalibrate_camera": {
            "type": "solution",
            "severity": "medium",
            "title": "Recalibrate the 3D Camera",
            "image": None,
            "video": None,
            "steps": [
                "The camera appears clean and undamaged but phantom detections persist even at max filter settings.",
                "The camera needs recalibration.",
                "Follow the guide 'How to calibrate a D435 3D camera' on MiR Support Portal.",
                "After calibration, test the robot's obstacle detection in the problem area.",
                "If the issue persists after recalibration, try a factory reset of the camera and recalibrate again.",
                "If still unresolved, contact MiR Technical Support with: robot serial number, description of the phantom detection, and a map screenshot.",
            ],
        },
    },
}
