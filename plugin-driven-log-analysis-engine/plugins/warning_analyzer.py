"""
Plugin to detect warning-level operational signals.
"""

from plugin_base import PluginBase


class WarningAnalyzer(PluginBase):
    """Detects WARNING log entries."""

    def __init__(self):
        super().__init__()
        self.name = "Warning Analyzer"
        self.description = "Detects warning keywords in logs"
        self.severity = "LOW"

    def analyze(self, log_line: str) -> dict:
        if "warning" in log_line.lower():
            return {
                "severity": self.severity,
                "message": "Warning detected",
                "details": {
                    "log_line": log_line.strip(),
                },
            }

        return None


def get_plugin():
    return WarningAnalyzer()
