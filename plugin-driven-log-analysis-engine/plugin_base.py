"""
Base class for all log analyzer plugins.
All plugins must inherit from this class.
"""


class PluginBase:
    """
    Base class that defines the interface for all analyzer plugins.
    """

    def __init__(self):
        self.name = "Base Plugin"
        self.description = "Base plugin class"
        self.severity = "INFO"

    def analyze(self, log_line: str) -> dict:
        """
        Analyze a single log line.

        Args:
            log_line: A single line from a log file

        Returns:
            Dictionary with analysis results or None if no match
        """
        raise NotImplementedError("Plugins must implement analyze() method")

    def get_info(self) -> dict:
        """
        Return plugin information.
        """
        return {
            "name": self.name,
            "description": self.description,
            "severity": self.severity,
        }
