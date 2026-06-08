"""
Plugin to detect privilege escalation indicators.
"""

from plugin_base import PluginBase


class PrivilegeEscalationAnalyzer(PluginBase):
    """Detects sudo and privilege escalation indicators."""

    def __init__(self):
        super().__init__()
        self.name = "Privilege Escalation Analyzer"
        self.description = "Detects privilege escalation and sudo abuse indicators"
        self.severity = "HIGH"
        self.keywords = [
            "sudo:",
            "session opened for user root",
            "privilege escalation",
            "uid=0",
        ]

    def analyze(self, log_line: str) -> dict:
        log_lower = log_line.lower()

        for keyword in self.keywords:
            if keyword in log_lower:
                return {
                    "severity": self.severity,
                    "message": "Privilege escalation indicator detected",
                    "details": {
                        "indicator": keyword,
                        "log_line": log_line.strip(),
                    },
                }

        return None


def get_plugin():
    return PrivilegeEscalationAnalyzer()
