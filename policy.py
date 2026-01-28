import json
import os


class PolicyEngine:
    def __init__(self, policy_file="permissions.json"):
        self.policy_file = policy_file
        self.policy = self._load_policy()

    def _load_policy(self):
        if not os.path.exists(self.policy_file):
            raise RuntimeError("permissions.json not found")
        with open(self.policy_file) as f:
            return json.load(f)

    # ----------------------------
    # Decision logic
    # ----------------------------

    def is_allowed(self, tool_mode):
        if tool_mode == "guided":
            return self.policy["modes"]["guided"]["enabled"]
        return True

    def requires_confirmation(self, tool_mode):
        return self.policy["modes"].get(tool_mode, {}).get(
            "confirmation_required", True
        )

    def exploitation_allowed(self):
        return self.policy["global"].get("allow_exploitation", False)

    def describe(self, tool_mode):
        return self.policy["modes"].get(tool_mode, {}).get(
            "description", "Unknown execution mode"
        )
