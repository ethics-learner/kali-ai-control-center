import subprocess
import threading
import time


class GuidedMetasploit:
    """
    Guided Metasploit launcher.
    Does NOT automate exploits.
    Guides the human operator step-by-step.
    """

    def __init__(self, output_callback, summary_callback):
        self.output_callback = output_callback
        self.summary_callback = summary_callback

    # ----------------------------
    # Entry point
    # ----------------------------

    def start(self):
        self.output_callback("[*] Guided Metasploit mode initiated.\n")
        self.output_callback("[*] Launching msfconsole...\n")
        self.output_callback("[*] This will open an interactive Metasploit session.\n\n")

        self._show_guidelines()
        self._launch_msfconsole()

    # ----------------------------
    # Guidance
    # ----------------------------

    def _show_guidelines(self):
        guidance = (
            "GUIDED METASPLOIT MODE\n"
            "=======================\n"
            "You are entering an interactive exploitation framework.\n\n"
            "Rules:\n"
            "- Do NOT target systems without authorization\n"
            "- Use this only for labs, testing, or permitted environments\n"
            "- You are responsible for every command you run\n\n"
            "Recommended workflow:\n"
            "1. search <service>\n"
            "2. use <module>\n"
            "3. show options\n"
            "4. set RHOSTS <target>\n"
            "5. run / exploit\n\n"
        )

        self.summary_callback(guidance)

    # ----------------------------
    # Launch Metasploit
    # ----------------------------

    def _launch_msfconsole(self):
        def run():
            try:
                subprocess.run(["msfconsole"])
            except Exception as e:
                self.output_callback(f"[ERROR] Failed to launch msfconsole: {e}\n")

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
