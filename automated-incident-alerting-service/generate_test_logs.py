#!/usr/bin/env python3

import time

from datetime import datetime

def generate_log_entry(event_type):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    events = {

        "failed_login":
        f"{timestamp} sshd[1234]: Failed password for admin from 192.168.1.100",

        "root_access":
        f"{timestamp} su: root login on tty1",

        "port_scan":
        f"{timestamp} firewall: port scan detected from 10.0.0.50",

        "normal":
        f"{timestamp} sshd[5678]: Accepted publickey for user from 192.168.1.10"
    }

    return events.get(
        event_type,
        events["normal"]
    )

if __name__ == "__main__":

    print(
        "[*] Generating test security logs..."
    )

    with open(
        "logs/security.log",
        "a"
    ) as f:

        for i in range(5):

            f.write(
                generate_log_entry(
                    "failed_login"
                ) + "\n"
            )

            f.flush()

            time.sleep(1)

        f.write(
            generate_log_entry(
                "root_access"
            ) + "\n"
        )

        f.flush()

        time.sleep(1)

        for i in range(2):

            f.write(
                generate_log_entry(
                    "port_scan"
                ) + "\n"
            )

            f.flush()

            time.sleep(1)

    print(
        "[+] Test logs generated successfully"
    )
