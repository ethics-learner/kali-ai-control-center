import subprocess
import threading
import json
from ai_summary import AISummarizer
from policy import PolicyEngine
from guided_msf import GuidedMetasploit
from report_generator import CaseReport


class ToolController:
    def __init__(self, output_callback, summary_callback, confirm_callback):
        self.output_callback = output_callback
        self.summary_callback = summary_callback
        self.confirm_callback = confirm_callback

        self.summarizer = AISummarizer()
        self.policy = PolicyEngine()
        self.report = CaseReport()
        self.tools = self._load_tools()

    # ----------------------------
    # Load tools
    # ----------------------------

    def _load_tools(self):
        try:
            with open("tools.json") as f:
                return json.load(f)
        except Exception:
            return {}

    # ----------------------------
    # Intent router
    # ----------------------------

    def run(self, intent_text):
        self.report.log_action(f"User request: {intent_text}")
        intent = intent_text.lower()

        if "tor" in intent:
            self._run_thread(self._tor_logs)
            return

        if "ssh" in intent:
            self._run_thread(self._ssh_logs)
            return

        if "scan" in intent or "nmap" in intent:
            self._run_thread(lambda: self._nmap_scan(intent))
            return

        for name, meta in self.tools.items():
            if name in intent:
                self._handle_tool(meta)
                return

        self.output_callback("[!] No matching tool found.\n")
        self.summary_callback("No tool matched your request.")

    # ----------------------------
    # Thread helper
    # ----------------------------

    def _run_thread(self, target):
        threading.Thread(target=target, daemon=True).start()

    # ----------------------------
    # Tool handler
    # ----------------------------

    def _handle_tool(self, tool):
        name = tool["name"]
        mode = tool["mode"]

        self.report.log_action(f"Tool requested: {name} ({mode})")

        if not self.policy.is_allowed(mode):
            msg = f"Execution blocked by policy for tool: {name}"
            self.summary_callback(msg)
            self.report.log_finding(msg)
            return

        if self.policy.requires_confirmation(mode):
            approved = self.confirm_callback(
                f"Tool: {name}\nMode: {mode.upper()}\nProceed?"
            )
            if not approved:
                msg = f"User cancelled execution of tool: {name}"
                self.summary_callback(msg)
                self.report.log_finding(msg)
                return

        if mode == "guided" and name == "msfconsole":
            GuidedMetasploit(self.output_callback, self.summary_callback).start()
            self.report.log_action("Guided Metasploit session started")
            return

        self.summary_callback(f"Tool {name} approved (execution not automated).")

    # ----------------------------
    # Built-in tools
    # ----------------------------

    def _tor_logs(self):
        output = self._collect(["journalctl", "-u", "tor", "--no-pager", "-n", "50"])
        summary = self.summarizer.summarize("tor", output)
        self.summary_callback(summary)
        self.report.log_finding(summary)

    def _ssh_logs(self):
        output = self._collect(["journalctl", "-u", "ssh", "--no-pager", "-n", "50"])
        summary = self.summarizer.summarize("ssh", output)
        self.summary_callback(summary)
        self.report.log_finding(summary)

    def _nmap_scan(self, intent):
        target = self._extract_target(intent)
        if not target:
            summary = "No target provided for network scan."
            self.summary_callback(summary)
            self.report.log_finding(summary)
            return

        output = self._collect(["nmap", "-sV", "-T4", "--top-ports", "100", target])
        summary = self.summarizer.summarize("nmap", output)
        self.summary_callback(summary)
        self.report.log_finding(summary)

    # ----------------------------
    # Helpers
    # ----------------------------

    def _extract_target(self, text):
        for p in text.split():
            if "." in p:
                return p
        return None

    def _collect(self, cmd):
        collected = ""
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in p.stdout:
            collected += line
            self.output_callback(line)
        return collected

    # ----------------------------
    # Report export
    # ----------------------------

    def export_report(self):
        return self.report.generate_pdf()
