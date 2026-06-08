#!/usr/bin/env python3

from datetime import datetime
import os

class AlertFormatter:

    def __init__(self, notification_config):

        self.notification = notification_config
        self.log_file = notification_config.get(
            "log_file",
            "alerts/incidents.log"
        )

    def format_alert(
        self,
        rule_name,
        severity,
        log_entry,
        count
    ):

        return f"""
============================================================
SECURITY ALERT
============================================================
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Rule: {rule_name}
Severity: {severity.upper()}
Occurrences: {count}
Log Entry: {log_entry.strip()}
============================================================
"""

    def send_alert(self, alert_message):

        if self.notification.get("console_enabled", True):
            print(alert_message)

        self.write_to_log(alert_message)

    def write_to_log(self, message):

        os.makedirs(
            os.path.dirname(self.log_file),
            exist_ok=True
        )

        with open(self.log_file, "a") as f:

            f.write(
                f"\n[{datetime.now()}]\n"
            )

            f.write(message)

            f.write("\n" + "-" * 80 + "\n")

if __name__ == "__main__":

    config = {
        "log_file": "alerts/incidents.log",
        "console_enabled": True
    }

    formatter = AlertFormatter(config)

    alert = formatter.format_alert(
        "Failed Login Attempt",
        "medium",
        "Failed password for admin",
        3
    )

    formatter.send_alert(alert)
