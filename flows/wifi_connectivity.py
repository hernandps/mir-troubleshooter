FLOW = {
    "title": "Wi-Fi / Connectivity",
    "start": "q_connection_method",
    "nodes": {

        # ── PHASE 1: HOW ARE YOU CONNECTING? ─────────────────────────────────

        "q_connection_method": {
            "type": "question",
            "text": "How are you trying to connect to the robot?",
            "hint": "This determines whether the issue is with the robot's internal network or the site WiFi.",
            "info": (
                "Connection methods and robot IP addresses:\n"
                "• Service port (Ethernet cable directly to robot) → IP: 192.168.12.20\n"
                "• Robot WiFi hotspot (MiR-[serial]) → IP: 192.168.12.20\n"
                "• Site WiFi (client network) → IP assigned by your router (varies)\n\n"
                "⚠️ If you don't know the site WiFi IP, use the service port or robot WiFi hotspot first.\n"
                "Also: contact your IT department — connection issues often occur if the robot was assigned a new IP or is on the wrong subnet."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Service port or robot WiFi hotspot",  "next": "q_ping_switch",   "style": "neutral"},
                {"label": "Site WiFi (client/plant network)",    "next": "q_site_wifi",     "style": "neutral"},
            ],
        },

        "q_site_wifi": {
            "type": "question",
            "text": "Can you connect to the robot using the service port or robot WiFi hotspot instead?",
            "hint": "This isolates whether the problem is with the site network or the robot itself.",
            "info": (
                "Try a direct connection:\n"
                "• Service port: plug an Ethernet cable from the robot's service port directly to your laptop.\n"
                "  Set your laptop's static IP to 192.168.12.30–40, then open 192.168.12.20 in a browser.\n"
                "• Robot WiFi hotspot: connect to 'MiR-[serial number]' WiFi → open 192.168.12.20 in a browser.\n\n"
                "Note: If you just updated the robot software, wait 5 minutes before trying again."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — I can reach the robot via service port or hotspot", "next": "sol_site_network_issue",   "style": "good"},
                {"label": "No — robot is unreachable even directly",                 "next": "q_ping_switch",           "style": "warn"},
            ],
        },

        # ── PHASE 2: PING THE SWITCH ──────────────────────────────────────────

        "q_ping_switch": {
            "type": "question",
            "text": "Can you ping the robot's internal network switch?",
            "hint": "Connect to robot WiFi or service port, then open Command Prompt and run: ping 192.168.12.1",
            "info": (
                "Steps:\n"
                "1. Connect to robot via service port Ethernet or robot WiFi hotspot.\n"
                "   If using Ethernet cable: set your laptop's static IP to 192.168.12.30–40.\n"
                "2. Open Command Prompt.\n"
                "3. Run:  ping 192.168.12.1\n"
                "4. A successful ping returns replies for most of the 4 packets sent.\n\n"
                "The internal switch (IP 192.168.12.1) connects the robot computer, PLC, scanners, and power board."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — switch responds to ping",  "next": "q_ping_computer", "style": "good"},
                {"label": "No — no response from switch",   "next": "q_switch_powered", "style": "warn"},
            ],
        },

        # ── PHASE 3: PING THE ROBOT COMPUTER ─────────────────────────────────

        "q_ping_computer": {
            "type": "question",
            "text": "Can you ping the robot computer?",
            "hint": "Open Command Prompt and run: ping 192.168.12.20",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — robot computer responds to ping", "next": "sol_site_network_issue",  "style": "good"},
                {"label": "No — no response from robot computer",  "next": "q_switch_to_computer",   "style": "warn"},
            ],
        },

        # ── PHASE 4: CHECK SWITCH → COMPUTER CONNECTION ───────────────────────

        "q_switch_to_computer": {
            "type": "question",
            "text": "Check inside the robot: is the network switch's port for the robot computer showing a connection (diode lit)?",
            "hint": "Access the front compartment. Check the diode on the switch for the robot computer port.",
            "info": (
                "Which port to check:\n"
                "• MiR250 hardware v1.0: port 2 diode\n"
                "• MiR250 hardware v2.0: port 5 diode\n"
                "• MiR600/MiR1350: check the Ethernet port diodes on the robot computer — green solid + yellow flashing/solid = connected\n\n"
                "⚠️ Robot must be ON when checking diodes.\n"
                "⚠️ Be careful of exposed electrical cables."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — diode is lit (connection present)",  "next": "q_network_scan",          "style": "good"},
                {"label": "No — diode is off (no connection)",        "next": "sol_reconnect_computer",  "style": "warn"},
            ],
        },

        "q_network_scan": {
            "type": "question",
            "text": "Scan the robot's internal network — is the robot computer IP (192.168.12.20) visible?",
            "hint": "Open a browser, go to 192.168.12.1/webfig/ (login: root / password: mirex), then Tools → IP Scan, range 192.168.10.0/24.",
            "info": (
                "Expected IP addresses in the scan result:\n"
                "• 192.168.12.1    (internal switch)\n"
                "• 192.168.12.9    (safety PLC)\n"
                "• 192.168.12.10   (front laser scanner)\n"
                "• 192.168.12.11   (rear laser scanner)\n"
                "• 192.168.12.20   (robot computer) ← look for this one\n"
                "• 192.168.12.100  (power board)\n\n"
                "If 192.168.12.20 is missing, the robot computer IP has not been assigned correctly."
            ),
            "image": None,
            "video": None,
            "options": [
                {"label": "192.168.12.20 is missing — others are present",       "next": "sol_switch_script",      "style": "warn"},
                {"label": "Multiple IPs are missing (less than 6 total)",        "next": "sol_switch_script",      "style": "warn"},
                {"label": "All 6 IPs present but web interface still won't load", "next": "sol_site_network_issue", "style": "neutral"},
            ],
        },

        # ── PHASE 5: SWITCH POWER ─────────────────────────────────────────────

        "q_switch_powered": {
            "type": "question",
            "text": "Check inside the robot: is the network switch showing any power (diodes/lights lit)?",
            "hint": "MiR250: any switch diodes lit. MiR600/1350: PWR diode at the top of the switch is lit.",
            "image": "assets/images/switch diodes MiR250.jpg",
            "video": None,
            "options": [
                {"label": "Yes — switch has lights/diodes on",   "next": "sol_switch_script",  "style": "good"},
                {"label": "No — switch has no lights at all",    "next": "q_switch_voltage",   "style": "warn"},
            ],
        },

        "q_switch_voltage": {
            "type": "question",
            "text": "Measure the voltage of the switch power cable. Does it deliver 19V?",
            "hint": "With robot ON: measure voltage relative to ground on the switch power cable inside the robot. Expected: ~19V.",
            "image": None,
            "video": None,
            "options": [
                {"label": "Yes — cable delivers ~19V",       "next": "sol_replace_switch", "style": "warn"},
                {"label": "No — voltage is low or 0V",      "next": "sol_power_board_j3", "style": "warn"},
            ],
        },

        # ── SOLUTIONS ─────────────────────────────────────────────────────────

        "sol_site_network_issue": {
            "type": "solution",
            "severity": "medium",
            "title": "Robot Is Reachable Directly — Site Network/IP Issue",
            "image": None,
            "video": None,
            "steps": [
                "The robot's internal network is working correctly, but site WiFi access is not working.",
                "Contact your IT department — connection issues over site WiFi typically occur when:",
                "• The robot was assigned a new IP address by the DHCP server.",
                "• The robot is no longer on the correct subnet or VLAN.",
                "• Another device was assigned the same IP address as the robot.",
                "Ask IT to configure a **static or DHCP-reserved IP address** for the robot in the network.",
                "Once you know the correct site WiFi IP, enter it in your browser to access the web interface.",
            ],
        },

        "sol_reconnect_computer": {
            "type": "solution",
            "severity": "medium",
            "title": "Ethernet Cable Between Switch and Robot Computer Is Disconnected",
            "image": None,
            "video": None,
            "steps": [
                "The Ethernet cable connecting the internal switch to the robot computer is disconnected or faulty.",
                "Reconnect the cable firmly at both ends (switch port and robot computer port).",
                "Try a spare Ethernet cable if available — the existing cable may be damaged.",
                "After reconnecting, wait ~30 seconds and try to ping 192.168.12.20 again.",
                "If the cable is firmly connected but still no connection, run the switch setup script.",
                "See guide: 'How to set up the router or Ethernet switch on MiR robots' (MiR Support Portal).",
            ],
        },

        "sol_switch_script": {
            "type": "solution",
            "severity": "medium",
            "title": "Run Switch Setup Script to Reassign IP Addresses",
            "image": None,
            "video": None,
            "steps": [
                "The robot computer IP (192.168.12.20) is not visible on the internal network — it has not been assigned correctly.",
                "Run the switch setup script to reassign the correct IP addresses.",
                "Follow the guide: **'How to set up the router or Ethernet switch on MiR robots'** (available on MiR Support Portal).",
                "After running the script, restart the robot and try to connect again.",
                "If the issue persists after running the script, contact MiR Technical Support.",
            ],
        },

        "sol_replace_switch": {
            "type": "solution",
            "severity": "hard",
            "title": "Switch Has 19V Power but Won't Start — Replace Switch",
            "image": None,
            "video": None,
            "steps": [
                "The power cable is delivering ~19V to the switch, but the switch is not powering on.",
                "First, run the switch setup script: see guide 'How to set up the router or Ethernet switch on MiR robots'.",
                "If the switch still does not power on after the setup script, the switch hardware is faulty.",
                "The switch needs to be replaced.",
                "Contact MiR Technical Support or your MiR distributor for a replacement switch.",
            ],
        },

        "sol_power_board_j3": {
            "type": "solution",
            "severity": "hard",
            "title": "Switch Power Cable Not Delivering 19V — Power Board Issue",
            "image": None,
            "video": None,
            "steps": [
                "The switch power cable is not delivering 19V — the issue is in the power supply upstream.",
                "Check that the **J3 connector** on the power board is securely connected.",
                "If J3 is connected but the cable still doesn't deliver 19V, the power board may be faulty.",
                "Check Monitoring → Hardware Health → Power System for any power-related errors.",
                "Contact MiR Technical Support with: robot serial number and the voltage reading you measured.",
            ],
        },
    },
}
