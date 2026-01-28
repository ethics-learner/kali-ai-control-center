import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


class CaseReport:
    def __init__(self):
        self.start_time = datetime.now()
        self.actions = []
        self.findings = []

        os.makedirs("reports", exist_ok=True)

    # ----------------------------
    # Logging
    # ----------------------------

    def log_action(self, text):
        self.actions.append(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — {text}"
        )

    def log_finding(self, text):
        self.findings.append(text)

    # ----------------------------
    # PDF generation
    # ----------------------------

    def generate_pdf(self, filename=None):
        if not filename:
            filename = f"reports/case_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(Paragraph("<b>Cyber Security Investigation Report</b>", styles["Title"]))
        story.append(Spacer(1, 20))

        # Metadata
        story.append(Paragraph("<b>Generated On:</b> " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), styles["Normal"]))
        story.append(Paragraph("<b>Session Started:</b> " + self.start_time.strftime("%Y-%m-%d %H:%M:%S"), styles["Normal"]))
        story.append(Spacer(1, 15))

        # Executive Summary
        story.append(Paragraph("<b>Executive Summary</b>", styles["Heading2"]))
        story.append(Paragraph(
            "This report documents the cybersecurity analysis and actions "
            "performed using the Kali AI Control Center. All actions were "
            "executed with user confirmation and under controlled conditions.",
            styles["Normal"]
        ))
        story.append(Spacer(1, 15))

        # Actions Timeline
        story.append(Paragraph("<b>Actions Timeline</b>", styles["Heading2"]))
        for act in self.actions:
            story.append(Paragraph(act, styles["Normal"]))
        story.append(Spacer(1, 15))

        # Findings
        story.append(Paragraph("<b>Findings & Analysis</b>", styles["Heading2"]))
        if self.findings:
            for f in self.findings:
                story.append(Paragraph(f, styles["Normal"]))
        else:
            story.append(Paragraph("No critical security findings were recorded.", styles["Normal"]))

        story.append(Spacer(1, 20))

        # Footer
        story.append(Paragraph(
            "This report was generated automatically by the Kali AI Control Center. "
            "All activities were performed in accordance with authorization and policy controls.",
            styles["Italic"]
        ))

        doc.build(story)
        return filename
