#!/usr/bin/env python3

import time
import random
from datetime import datetime


NORMAL_EVENTS = [
    "User login successful from 192.168.1.{} - user: employee{}",
    "File accessed: /home/user{}/documents/report.pdf",
    "Service started: web_server on port 80"
]

SUSPICIOUS_EVENTS = [
    "Failed login attempt from 10.0.0.{} - user: admin - attempt {}",
    "Port scan detected from 203.0.113.{} targeting ports 22,23,3389",
    "Unusual outbound connection to 198.51.100.{} on port 4444",
    "Multiple failed sudo attempts - user: guest{}"
]


def generate_log_entry(event_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if event_type == "suspicious":
        template = random.choice(SUSPICIOUS_EVENTS)
    else:
        template = random.choice(NORMAL_EVENTS)

    value_one = random.randint(1, 254)
    value_two = random.randint(1, 20)

    event = template.format(value_one, value_two)

    return f"{timestamp} | {event}"


def main():
    log_file = "logs/security.log"

    print("Starting log generation... Press Ctrl+C to stop.")

    with open(log_file, "a") as file:
        try:
            while True:
                event_type = "suspicious" if random.random() < 0.20 else "normal"
                log_entry = generate_log_entry(event_type)

                file.write(log_entry + "\n")
                file.flush()

                print(log_entry)
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nLog generation stopped.")


if __name__ == "__main__":
    main()
