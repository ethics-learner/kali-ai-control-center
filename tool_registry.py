import os
import json

# Common Kali tool locations
SEARCH_PATHS = [
    "/usr/bin",
    "/usr/sbin",
    "/bin",
    "/sbin"
]

# Very simple keyword-based categorization
CATEGORY_MAP = {
    "nmap": "Network Scanning",
    "nikto": "Web Testing",
    "gobuster": "Web Testing",
    "dirsearch": "Web Testing",
    "sqlmap": "Web Testing",
    "hydra": "Password Attacks",
    "john": "Password Attacks",
    "aircrack": "Wireless",
    "airodump": "Wireless",
    "tshark": "Forensics",
    "tcpdump": "Forensics",
    "volatility": "Forensics",
    "msfconsole": "Exploitation",
    "metasploit": "Exploitation"
}

DEFAULT_CATEGORY = "Other"


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    # ----------------------------
    # Scan system for tools
    # ----------------------------

    def discover(self):
        for base in SEARCH_PATHS:
            if not os.path.isdir(base):
                continue

            for name in os.listdir(base):
                path = os.path.join(base, name)

                if not os.path.isfile(path):
                    continue

                if not os.access(path, os.X_OK):
                    continue

                if name in self.tools:
                    continue

                category = self._categorize(name)

                self.tools[name] = {
                    "name": name,
                    "path": path,
                    "category": category,
                    "mode": self._execution_mode(category)
                }

        return self.tools

    # ----------------------------
    # Categorization
    # ----------------------------

    def _categorize(self, tool_name):
        for key, cat in CATEGORY_MAP.items():
            if key in tool_name.lower():
                return cat
        return DEFAULT_CATEGORY

    # ----------------------------
    # Execution policy
    # ----------------------------

    def _execution_mode(self, category):
        if category in ["Network Scanning", "Forensics", "Logs & Monitoring"]:
            return "auto"

        if category in ["Web Testing", "Password Attacks", "Wireless"]:
            return "assisted"

        if category == "Exploitation":
            return "guided"

        return "assisted"

    # ----------------------------
    # Save registry
    # ----------------------------

    def save(self, filename="tools.json"):
        with open(filename, "w") as f:
            json.dump(self.tools, f, indent=2)

    # ----------------------------
    # Load registry
    # ----------------------------

    def load(self, filename="tools.json"):
        if not os.path.exists(filename):
            return {}
        with open(filename) as f:
            self.tools = json.load(f)
        return self.tools


if __name__ == "__main__":
    registry = ToolRegistry()
    registry.discover()
    registry.save()
    print(f"[+] Discovered {len(registry.tools)} tools.")

