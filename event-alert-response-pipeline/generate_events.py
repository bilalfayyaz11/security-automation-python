#!/usr/bin/env python3
"""
Security Event Generator

Simulates security events for testing the alert response pipeline.
"""

from datetime import datetime
from pathlib import Path
import time


def generate_event(event_type: str, source_ip: str, details: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp} | {source_ip} | {event_type} | {details}\n"


def main() -> None:
    events = [
        ("FAILED_LOGIN", "192.168.1.100", "User: admin"),
        ("FAILED_LOGIN", "192.168.1.100", "User: root"),
        ("FAILED_LOGIN", "192.168.1.100", "User: admin"),
        ("UNAUTHORIZED_ACCESS", "10.0.0.50", "File: /etc/shadow"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 22,80,443,3306"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 8080,8443"),
        ("NORMAL_LOGIN", "192.168.1.10", "User: john"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 21,23,25"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 3389,5900"),
        ("PORT_SCAN", "172.16.0.25", "Ports: 1433,5432"),
        ("PRIVILEGE_ESCALATION", "10.0.0.75", "Process attempted UID 0 escalation"),
    ]

    output_path = Path("logs/security_events.log")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Generating security events...")

    with output_path.open("a", encoding="utf-8") as file:
        for event_type, ip, details in events:
            log_entry = generate_event(event_type, ip, details)
            file.write(log_entry)
            print(f"Generated: {event_type} from {ip}")
            time.sleep(0.2)

    print("\nEvent generation complete!")


if __name__ == "__main__":
    main()
