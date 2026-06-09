#!/usr/bin/env python3

import re
import time
from datetime import datetime


THREAT_PATTERNS = {
    "brute_force": r"Failed login attempt.*user: admin",
    "port_scan": r"Port scan detected",
    "suspicious_connection": r"Unusual outbound connection.*port 4444",
    "privilege_escalation": r"Multiple failed sudo attempts"
}


def analyze_log_line(line):
    for threat_type, pattern in THREAT_PATTERNS.items():
        if re.search(pattern, line, re.IGNORECASE):
            return {
                "threat_type": threat_type,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "raw_log": line.strip()
            }

    return None


def monitor_logs(log_file, alert_file):
    print(f"Monitoring {log_file} for threats...")

    with open(log_file, "r") as log:
        log.seek(0, 2)

        while True:
            line = log.readline()

            if not line:
                time.sleep(0.5)
                continue

            threat = analyze_log_line(line)

            if threat:
                alert = (
                    f"{threat['timestamp']} | "
                    f"THREAT={threat['threat_type']} | "
                    f"RAW_LOG={threat['raw_log']}"
                )

                with open(alert_file, "a") as alerts:
                    alerts.write(alert + "\n")

                print(f"[ALERT] {alert}")


def main():
    log_file = "logs/security.log"
    alert_file = "alerts/threats.txt"

    monitor_logs(log_file, alert_file)


if __name__ == "__main__":
    main()
