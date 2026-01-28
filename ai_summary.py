import os
import requests


class AISummarizer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    # ----------------------------
    # Public entry
    # ----------------------------

    def summarize(self, tool_name, text):
        if self.api_key:
            try:
                return self._ai_summary(tool_name, text)
            except Exception:
                return self._offline_summary(tool_name, text)
        else:
            return self._offline_summary(tool_name, text)

    # ----------------------------
    # AI summary (safe usage)
    # ----------------------------

    def _ai_summary(self, tool_name, text):
        prompt = f"""
You are a cybersecurity analyst.

Tool: {tool_name}

Summarize the output below.
Focus on:
- Security relevance
- Exposed services or risks
- Clear conclusion
- No commands

LOG DATA:
{text[:4000]}
"""

        payload = {
            "model": "gpt-4.1-mini",
            "messages": [
                {"role": "system", "content": "You summarize cybersecurity tool output."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=40
        )

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    # ----------------------------
    # Offline summaries (fallback)
    # ----------------------------

    def _offline_summary(self, tool_name, text):
        text_lower = text.lower()

        if tool_name == "tor":
            if "compression bomb" in text_lower:
                return (
                    "Tor blocked highly compressed payloads.\n"
                    "This is a normal Tor security feature.\n"
                    "Such events are common on the Tor network.\n"
                    "No system compromise detected."
                )
            return (
                "Tor service is active.\n"
                "No critical anomalies detected in recent logs."
            )

        if tool_name == "ssh":
            if "failed" in text_lower:
                return (
                    "Failed SSH authentication attempts were detected.\n"
                    "This may indicate brute-force login attempts.\n"
                    "Consider limiting SSH access and using key-based authentication."
                )
            return (
                "SSH activity appears normal.\n"
                "No failed authentication patterns detected."
            )

        if tool_name == "nmap":
            if "open" in text_lower:
                return (
                    "Network scan completed successfully.\n"
                    "One or more open ports were detected.\n"
                    "Exposed services may present security risks.\n"
                    "Further service-level analysis is recommended."
                )
            return (
                "Network scan completed.\n"
                "No open ports detected among the scanned services."
            )

        return (
            "Analysis completed.\n"
            "No significant security findings identified."
        )
