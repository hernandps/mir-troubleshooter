FLOW = {
    "title": "Robot Not Starting",
    "start": "q_power_button_color",
    "nodes": {

        # ── PHASE 1: POWER BUTTON COLOR ───────────────────────────────────────

        "q_power_button_color": {
            "type": "question",
            "text": "Press the Power button on the robot. What color does it light up?",
            "hint": "The Power button is on the side of the robot. It tells you the battery state immediately.",
            "info": (
                "Power button color meanings:\n"
                "• Green → robot has power, likely a switch/computer/software issue\n"
                "• Red → battery is critically low\n"
                "• No light at all → no power from battery at all"
            ),
            "image": "assets/images/power button MiR600.jpg",
            "video": None,
            "options": [
                {"label": "Green — robot has power",   "next": "q_status_lights",       "style": "good"},
                {"label": "Red — battery critically low", "next": "q_can_charge",        "style": "warn"},
                {"label": "No light at all",            "next": "q_battery_connected",  "style": "warn"},
            ],
        },

        # ── PATH: GREEN POWER BUTTON ──────────────────────────────────────────

        "q_status_lights": {
            "type": "question",
            "text": "Do the status lights (top strip) keep wavering yellow?",
            "hint": "Wavering yellow = robot is still starting up. This should take less than a minute normally, longer after a software update.",
            "image": "assets/images/MiR250 yellow status lights.jpg",
            "video": None,
            "options": [
                {"label": "Yes — lights keep wavering yellow", "next": "q_computer_power_button", "style": "warn"},
                {"label": "No lights at all (strip is dark)",   "next": "sol_no_status_lights",   "style": "warn"},
                {"label": "Lights changed to red or another color", "next": "sol_lights_changed", "style": "good"},
            ],
        },

        "q_computer_power_button": {
            "type": "question",
            "text": "Open the robot's front compartment and check the Power button on the robot computer. Is it lit up?",
            "hint": "The robot computer is a small PC inside the front compartment. Its power button is on the front of the unit.",
            "info": (
                "Access the front compartment:\n"
                "• MiR250: remove the front cover panel\n"
                "• MiR600/1350: open the front electronics drawer\n\n"
                "⚠️ Battery must be connected and robot powered on for this check.\n"
                "⚠️ Be careful of exposed electrical cables."
            ),
            "image": [
                "assets/images/robot computer power button MiR250.jpg",
                "assets/images/robot computer power button MiR600.jpg",
            ],
            "video": None,
            "options": [
                {"label": "Yes — computer power button is ON",  "next": "q_ping_computer_startup", "style": "good"},
                {"label": "No — computer power button is OFF",  "next": "q_manual_computer_on",    "style": "warn"},
            ],
        },

        "q_manual_computer_on": {
            "type": "question",
            "text": "Press the Power button directly on the robot computer. Does it start up?",
            "hint": "Press the button and wait a few seconds. Check if the button LED comes on and any fan/disk activity starts.",
            "image": [
                "assets/images/robot computer power button MiR250.jpg",
                "assets/images/robot computer power button MiR600.jpg",
            ],
            "video": None,
            "options": [
                {"label": "Yes — computer started up manually", "next": "q_startup_successful",    "style": "good"},
                {"label": "No — computer won't turn on at all",  "next": "sol_computer_no_power",  "style": "warn"},
            ],
        },

        "q_startup_successful": {
            "type": "question",
            "text": "After the computer started, turn it off and on again normally. Does the computer start by itself this time?",
            "hint": "Wait at least 1 minute after full startup. Also check Monitoring → Hardware Health for any errors.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — starts by itself now (was a one-time issue)", "next": "sol_startup_ok",        "style": "good"},
                {"label": "Still needs to be started manually every time",      "next": "sol_bootup_cable",     "style": "warn"},
                {"label": "Hardware errors shown in the interface",             "next": "sol_hardware_errors",  "style": "warn"},
                {"label": "Cannot access the robot interface",                  "next": "sol_goto_connect",     "style": "warn"},
            ],
        },

        "q_ping_computer_startup": {
            "type": "question",
            "text": "The computer is ON but status lights are stuck yellow. Can you ping the robot computer?",
            "hint": "Connect to the robot via service port or WiFi hotspot. Open Command Prompt and run: ping 192.168.12.20",
            "info": (
                "Steps:\n"
                "1. Connect to robot via Ethernet service port (set your laptop IP to 192.168.12.30–40)\n"
                "   OR connect to the robot's WiFi hotspot (MiR-[serial])\n"
                "2. Open Command Prompt\n"
                "3. Run:  ping 192.168.12.20\n"
                "4. Check if you get replies"
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — ping responds",  "next": "sol_goto_connect",       "style": "good"},
                {"label": "No — no ping response", "next": "q_ping_power_board",    "style": "warn"},
            ],
        },

        "q_ping_power_board": {
            "type": "question",
            "text": "Open Monitoring → Hardware Health → Power System in the web interface. Are there any errors? Also try pinging the power board.",
            "hint": "Ping the power board: ping 192.168.12.100. The power board is a separate device from the robot computer.",
            "info": (
                "Power board IP: 192.168.12.100\n\n"
                "Run:  ping 192.168.12.100\n\n"
                "If you can't access the web interface, try the ping from Command Prompt while connected to the service port."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Power board ping responds — no errors",   "next": "sol_contact_support",       "style": "good"},
                {"label": "Power board errors visible in interface",  "next": "sol_power_board_ethernet",  "style": "warn"},
                {"label": "Power board ping fails — no response",    "next": "sol_power_board_ethernet",  "style": "warn"},
            ],
        },

        # ── PATH: RED POWER BUTTON ────────────────────────────────────────────

        "q_can_charge": {
            "type": "question",
            "text": "Connect a cable charger (3A charger) to the battery or robot charging port. Does the charger start charging?",
            "hint": "The charger LED changes color or it starts humming when charging is active. Let it charge at least 10 minutes before retrying.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — charger is charging the battery", "next": "sol_charge_and_retry", "style": "good"},
                {"label": "No — charger won't charge it",          "next": "sol_goto_battery",     "style": "warn"},
            ],
        },

        # ── PATH: NO LIGHT ────────────────────────────────────────────────────

        "q_battery_connected": {
            "type": "question",
            "text": "Check that the battery is correctly connected to the robot. Is the battery physically connected?",
            "hint": "Open the battery compartment and verify the battery connector is fully seated and the battery lever is in the locked position.",
            "image": None,
            "video": None,
            "options": [
                {"label": "No — battery was disconnected or not seated", "next": "sol_connect_battery", "style": "warn"},
                {"label": "Yes — battery is connected but still no power", "next": "sol_goto_battery",  "style": "warn"},
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────────

        "sol_no_status_lights": {
            "type": "solution",
            "severity": "hard",
            "title": "Status Lights Not On — Possible CAN Bus or Hardware Issue",
            "image": None,
            "video": None,
            "steps": [
                "Power button is green (power OK) but the status light strip is completely off.",
                "If you can access the robot interface, check Monitoring → Hardware Health for faults.",
                "If no errors show in Hardware Health, this may be a CAN bus or indicator light issue.",
                "Go to the 'CAN Bus / Lights Not Working' troubleshooting flow for a detailed diagnosis.",
                "If you cannot access the interface at all, contact MiR Technical Support.",
            ],
        },

        "sol_lights_changed": {
            "type": "solution",
            "severity": "easy",
            "title": "Robot Started — Status Lights Changed Color",
            "image": None,
            "video": None,
            "steps": [
                "The status lights changed from yellow to another color — the robot has started up.",
                "Red or flashing lights: the robot is in Protective or Emergency Stop.",
                "→ Go to the 'Constantly in Protective State' troubleshooting flow.",
                "If you cannot access the robot interface from your device, go to the 'Wi-Fi / Connectivity' flow.",
            ],
        },

        "sol_computer_no_power": {
            "type": "solution",
            "severity": "hard",
            "title": "Robot Computer Not Receiving Power",
            "image": None,
            "video": None,
            "steps": [
                "The robot computer is not turning on — it is not receiving power.",
                "Check the power cable connection from the Power Board to the robot computer.",
                "The power cable should deliver 19 V. Measure the voltage relative to ground to verify.",
                "If the cable delivers 19 V but the computer still won't turn on → the computer itself is faulty.",
                "If the cable does not deliver 19 V → the power board is not sending power correctly.",
                "Contact MiR Technical Support with: robot serial number, which component is suspected (power board or computer), and voltage reading.",
            ],
        },

        "sol_startup_ok": {
            "type": "solution",
            "severity": "easy",
            "title": "One-Time Startup Issue — Robot Is Now OK",
            "image": None,
            "video": None,
            "steps": [
                "The robot computer is now starting up correctly on its own.",
                "This appears to have been a one-time issue.",
                "If the problem returns (random failure to turn on), check the boot-up cable from the power board to the robot computer.",
                "The boot-up cable connects to the SW socket on the robot computer and the J3 socket on the power board.",
                "Monitor the robot for recurrence. If it happens again, contact MiR Technical Support.",
            ],
        },

        "sol_bootup_cable": {
            "type": "solution",
            "severity": "medium",
            "title": "Boot-Up Cable Issue — Computer Needs Manual Start Every Time",
            "image": [
                "assets/images/boot-up cable MiR250.jpg",
                "assets/images/boot-up cable MiR600.jpg",
            ],
            "video": None,
            "steps": [
                "The robot computer starts when pressed manually, but does not auto-start — the boot-up cable is likely faulty or disconnected.",
                "Locate the boot-up cable: it connects from the SW socket on the robot computer to the J3 socket on the power board.",
                "For MiR250: the cable is behind the robot computer (visible when front cover is removed).",
                "For MiR600/1350: the cable runs from the robot computer to the J3 connector on the power board in the electronics drawer.",
                "Check the cable is firmly connected at both ends. Try disconnecting and reconnecting it.",
                "If the cable is damaged, it must be replaced. Contact MiR Technical Support or your distributor.",
            ],
        },

        "sol_hardware_errors": {
            "type": "solution",
            "severity": "hard",
            "title": "Hardware Errors Detected After Startup",
            "image": None,
            "video": None,
            "steps": [
                "The robot computer started, but hardware errors are reported in Monitoring → Hardware Health.",
                "Note the exact error messages and which subsystem is affected.",
                "Cross-reference with the relevant troubleshooting flow based on the error type:",
                "→ Safety system errors: use the 'Constantly in Protective State' flow.",
                "→ CAN bus / light errors: use the 'CAN Bus / Lights' flow.",
                "→ Power system errors: see the 'Battery' or 'Not Starting' flow.",
                "If the error doesn't match any flow, contact MiR Technical Support with the error screenshot and robot serial number.",
            ],
        },

        "sol_goto_connect": {
            "type": "solution",
            "severity": "medium",
            "title": "Computer Is On But Interface Not Reachable",
            "image": None,
            "video": None,
            "steps": [
                "The robot computer started up (power button is on) but the web interface is not accessible.",
                "This is a connectivity issue — follow the 'Wi-Fi / Connectivity' troubleshooting flow.",
                "Check: are you on the correct network? Try the service port (Ethernet directly to robot).",
                "Service port IP: 192.168.12.20 — set your laptop's static IP to 192.168.12.30–40.",
            ],
        },

        "sol_power_board_ethernet": {
            "type": "solution",
            "severity": "hard",
            "title": "Power Board Not Responding — Check Ethernet Connection",
            "image": None,
            "video": None,
            "steps": [
                "The power board (IP 192.168.12.100) is not responding — there may be an Ethernet connection issue.",
                "Check the Ethernet cable connecting the switch to the power board inside the robot.",
                "If you have a spare Ethernet cable, disconnect the existing one and try a known-good cable.",
                "For MiR250: see the guide 'How to replace the Ethernet cable between router/switch and power board on MiR250' on MiR Support Portal.",
                "For MiR600/1350: replace the cable in the electronics drawer. Cut off the connectors on the faulty cable but do not attempt to remove it.",
                "If the replacement cable still doesn't ping, the power board itself may be faulty. Contact MiR Technical Support.",
            ],
        },

        "sol_charge_and_retry": {
            "type": "solution",
            "severity": "easy",
            "title": "Battery Was Critically Low — Charging",
            "image": None,
            "video": None,
            "steps": [
                "The battery is critically low (power button turned red).",
                "Leave the charger connected for at least 10 minutes.",
                "Then try pressing the Power button again.",
                "If the robot still won't turn on after charging, go to the 'Battery Issues' troubleshooting flow.",
            ],
        },

        "sol_goto_battery": {
            "type": "solution",
            "severity": "hard",
            "title": "Battery Cannot Be Charged — Battery Flow Needed",
            "image": None,
            "video": None,
            "steps": [
                "The battery is not responding to the charger or has no power at all.",
                "Go to the 'Battery Issues' troubleshooting flow for a full battery diagnosis.",
                "Key symptoms that lead here: power button doesn't light, or power button is red and won't charge.",
            ],
        },

        "sol_connect_battery": {
            "type": "solution",
            "severity": "easy",
            "title": "Battery Was Not Connected",
            "image": None,
            "video": None,
            "steps": [
                "The battery was not correctly connected to the robot.",
                "Reconnect the battery: insert it fully into the battery compartment and ensure the lever locks into position.",
                "Try pressing the Power button again.",
                "If the power button still doesn't light up after reconnecting the battery, go to the 'Battery Issues' flow.",
            ],
        },

        "sol_contact_support": {
            "type": "solution",
            "severity": "hard",
            "title": "Power Board OK But Status Lights Stuck Yellow — Escalate",
            "image": None,
            "video": None,
            "steps": [
                "The power board responds (ping 192.168.12.100 succeeds) but the robot computer is not pinging and the status lights stay yellow.",
                "The Ethernet connection between the switch and robot computer may be faulty, or the computer is crashed.",
                "Try connecting to the switch at 192.168.12.1 in a browser — go to Tools → IP Scan → 192.168.10.0/24 to see which devices are visible.",
                "If 192.168.12.20 (robot computer) is missing from the list, the computer is not connecting to the network.",
                "Try reseating the Ethernet cable from the switch to the robot computer.",
                "If the issue persists, contact MiR Technical Support with: robot serial number, IP scan screenshot, and description of the startup behavior.",
            ],
        },
    },
}
