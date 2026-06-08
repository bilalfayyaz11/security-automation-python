#!/usr/bin/env python3

import time
import yaml
import re

from collections import defaultdict

from alert_formatter import AlertFormatter

class IntegratedAlertSystem:

    def __init__(self, config_file):

        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        self.rules = config["alert_rules"]

        self.formatter = AlertFormatter(
            config["notification"]
        )

        self.incident_counts = defaultdict(int)

    def process_log_line(self, line):

        for rule in self.rules:

            if re.search(
                rule["pattern"],
                line,
                re.IGNORECASE
            ):

                self.incident_counts[
                    rule["name"]
                ] += 1

                count = self.incident_counts[
                    rule["name"]
                ]

                if count >= rule["threshold"]:

                    alert = self.formatter.format_alert(
                        rule["name"],
                        rule["severity"],
                        line,
                        count
                    )

                    self.formatter.send_alert(
                        alert
                    )

                    self.incident_counts[
                        rule["name"]
                    ] = 0

    def monitor(self, log_file):

        print(
            f"[*] Monitoring {log_file} for security incidents..."
        )

        with open(log_file, "r") as f:

            f.seek(0, 2)

            while True:

                line = f.readline()

                if not line:
                    time.sleep(1)
                    continue

                self.process_log_line(line)

if __name__ == "__main__":

    system = IntegratedAlertSystem(
        "config/alert_config.yaml"
    )

    system.monitor(
        "logs/security.log"
    )
