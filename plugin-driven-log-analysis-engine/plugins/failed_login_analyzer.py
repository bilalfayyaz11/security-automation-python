"""
Plugin to detect failed login attempts in logs.
"""

import re
from plugin_base import PluginBase


class FailedLoginAnalyzer(PluginBase):
    """Detects failed SSH, PAM, and sudo authentication attempts."""

    def __init__(self):
        super().__init__()
        self.name = "Failed Login Analyzer"
        self.description = "Detects failed authentication attempts"
        self.severity = "HIGH"
        self.patterns = [
            r"Failed password for (?P<user>\S+) from (?P<src_ip>[\d\.]+)",
            r"authentication failure.*rhost=(?P<src_ip>[\d\.]+)",
            r"sudo: authentication failure for user (?P<user>\S+)",
        ]

    def analyze(self, log_line: str) -> dict:
        for pattern in self.patterns:
            match = re.search(pattern, log_line, re.IGNORECASE)

            if match:
                return {
                    "severity": self.severity,
                    "message": "Failed login attempt detected",
                    "details": {
                        "pattern_matched": pattern,
                        "entities": {key: value for key, value in match.groupdict().items() if value},
                        "log_line": log_line.strip(),
                    },
                }

        return None


def get_plugin():
    return FailedLoginAnalyzer()
