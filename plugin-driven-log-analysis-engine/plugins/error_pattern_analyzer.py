"""
Plugin to detect common error patterns in logs.
"""

from plugin_base import PluginBase


class ErrorPatternAnalyzer(PluginBase):
    """Detects common error keywords in logs."""

    def __init__(self):
        super().__init__()
        self.name = "Error Pattern Analyzer"
        self.description = "Detects error keywords and failure patterns"
        self.error_keywords = {
            "critical": "CRITICAL",
            "fatal": "CRITICAL",
            "exception": "MEDIUM",
            "error": "MEDIUM",
        }

    def analyze(self, log_line: str) -> dict:
        log_lower = log_line.lower()

        for keyword, severity in self.error_keywords.items():
            if keyword in log_lower:
                return {
                    "severity": severity,
                    "message": f"Error keyword detected: {keyword}",
                    "details": {
                        "keyword": keyword,
                        "log_line": log_line.strip(),
                    },
                }

        return None


def get_plugin():
    return ErrorPatternAnalyzer()
