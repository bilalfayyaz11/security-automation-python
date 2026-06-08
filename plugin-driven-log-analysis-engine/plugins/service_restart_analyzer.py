"""
Plugin to detect service restart activity.
"""

from plugin_base import PluginBase


class ServiceRestartAnalyzer(PluginBase):
    """Detects service restart events."""

    def __init__(self):
        super().__init__()
        self.name = "Service Restart Analyzer"
        self.description = "Detects service restart events"
        self.severity = "LOW"

    def analyze(self, log_line: str) -> dict:
        if "service restarted" in log_line.lower():
            return {
                "severity": self.severity,
                "message": "Service restart detected",
                "details": {
                    "log_line": log_line.strip(),
                },
            }

        return None


def get_plugin():
    return ServiceRestartAnalyzer()
