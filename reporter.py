import datetime
from pathlib import Path
from config import settings
from models import SessionState

class SecurityReporter:
    """
    Compiles the finalized autonomous session states into a highly structured,
    executive-ready Markdown penetration testing report.
    """

    def __init__(self, session_state: SessionState):
        self.state = session_state
        # Output layout: cyberguard-ai/reports/report_sessionID.md
        self.output_path: Path = settings.REPORT_DIR / f"report_{self.state.session_id}.md"

    def generate_markdown_report(self) -> Path:
        """
        Parses session history, actions taken, and vulnerabilities found 
        to compile a clean Markdown security audit artifact.
        """
        print(f"[*] Compiling executive security report for session {self.state.session_id}...")

        report_lines = [
            f"# CyberGuard AI — Automated Security Assessment Report",
            f"**Generated On:** {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
            f"\n## 1. Executive Summary",
            f"CyberGuard AI has completed an authorized security assessment against target asset: `{self.state.target}`.",
            f"The assessment started at `{self.state.start_time}` and systematically processed the asset vector space.",
            f"\n### Found Insights & Milestones Summary",
        ]

        # 1. Populate general insights summaries
        if self.state.findings_summary:
            for finding in self.state.findings_summary:
                report_lines.append(f"* [i] {finding}")
        else:
            report_lines.append("* No high-level narrative summaries were explicitly recorded during this run.")

        # 2. Add structural network topology information
        report_lines.append("\n## 2. Network Attack Surface Discovery")
        if self.state.discovered_host_info and self.state.discovered_host_info.open_ports:
            report_lines.append("The initial discovery scan identified the following exposed network ports:")
            report_lines.append("\n| Port | Protocol | State | Identified Service |")
            report_lines.append("| :--- | :--- | :--- | :--- |")
            for port in self.state.discovered_host_info.open_ports:
                report_lines.append(f"| `{port.port}` | {port.protocol.upper()} | **{port.state}** | {port.service} |")
        else:
            report_lines.append("`[!]` Warning: No active open ports or running service profiles were flagged on the target.")

        # 3. Add chronological execution steps
        report_lines.append("\n## 3. Autonomous Execution & Intelligence Logs")
        report_lines.append("The table below details the sequential deep-dives chosen by the AI reasoning core:")
        if self.state.actions_taken:
            report_lines.append("\n| # | Applied Security Tool | Target Context/Arguments | Execution Extract Summary |")
            report_lines.append("| :--- | :--- | :--- | :--- |")
            for index, action in enumerate(self.state.actions_taken, 1):
                # Clean up nested arguments layout for elegant table insertion
                arg_str = ", ".join([f"{k}: {v}" for k, v in action.arguments.items()])
                # Truncate overly verbose response data rows neatly
                clean_summary = action.result_summary.replace("\n", " ").strip()
                if len(clean_summary) > 120:
                    clean_summary = f"{clean_summary[:117]}..."
                
                report_lines.append(f"| {index} | `{action.tool_name}` | `{arg_str}` | {clean_summary} |")
        else:
            report_lines.append("* No complex downstream toolchains were recorded for this operational session.")

        # 4. Add professional remediation signoff footer
        report_lines.append("\n---")
        report_lines.append("\n## 4. Security Framework & Disclaimer Notice")
        report_lines.append(
            "> **CONFIDENTIALITY NOTICE:** This artifact contains highly privileged technical assessment "
            "metrics regarding the specified target environment. This document must be managed securely "
            "and restricted to authorized personnel only.\n\n"
            "**Remediation Guidance:** All software suites flagged as outdated or unnecessarily exposed via standard "
            "network vectors should be immediately updated to their latest long-term stable variants, hardened using "
            "principle-of-least-privilege firewall rule alignments, and re-audited."
        )

        # Write output block to file
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(report_lines))
            print(f"[+] Report compiled and written successfully to: {self.output_path.name}")
            return self.output_path
        except Exception as e:
            print(f"[!] Failed to write markdown report to file system: {e}")
            raise e