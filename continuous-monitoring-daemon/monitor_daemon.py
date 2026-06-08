#!/usr/bin/env python3

import time
import sys

from datetime import datetime

class LogMonitor:

    def __init__(
        self,
        log_file,
        output_file,
        replay_speed=1.0
    ):

        self.log_file = log_file
        self.output_file = output_file
        self.replay_speed = replay_speed
        self.alert_count = 0

    def parse_log_line(self, line):

        parts = line.strip().split(' ', 3)

        if len(parts) < 4:
            return None

        return {
            'date': parts[0],
            'time': parts[1],
            'level': parts[2],
            'message': parts[3]
        }

    def check_alert_conditions(self, log_entry):

        level = log_entry.get(
            'level',
            ''
        )

        return level in [
            'ERROR',
            'CRITICAL'
        ]

    def write_alert(self, log_entry):

        timestamp = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        alert_msg = (
            f"[ALERT {timestamp}] "
            f"{log_entry['level']}: "
            f"{log_entry['message']}\n"
        )

        with open(
            self.output_file,
            'a'
        ) as f:

            f.write(alert_msg)

        self.alert_count += 1

        print(
            f"ALERT: "
            f"{log_entry['level']} - "
            f"{log_entry['message']}"
        )

    def run(self):

        print(
            "Starting monitoring daemon..."
        )

        print(
            f"Reading from: {self.log_file}"
        )

        print(
            f"Writing alerts to: {self.output_file}"
        )

        print(
            f"Replay speed: {self.replay_speed}x"
        )

        print("-" * 60)

        try:

            with open(
                self.log_file,
                'r'
            ) as f:

                lines = f.readlines()

            for line in lines:

                log_entry = self.parse_log_line(
                    line
                )

                if log_entry is None:
                    continue

                print(
                    f"[{log_entry['date']} "
                    f"{log_entry['time']}] "
                    f"{log_entry['level']}: "
                    f"{log_entry['message']}"
                )

                if self.check_alert_conditions(
                    log_entry
                ):

                    self.write_alert(
                        log_entry
                    )

                time.sleep(
                    0.5 /
                    self.replay_speed
                )

            print("-" * 60)

            print(
                f"Monitoring complete. "
                f"Total alerts: "
                f"{self.alert_count}"
            )

        except FileNotFoundError:

            print(
                f"ERROR: Log file not found: "
                f"{self.log_file}"
            )

            sys.exit(1)

        except KeyboardInterrupt:

            print(
                "\nMonitoring stopped by user"
            )

            print(
                f"Total alerts generated: "
                f"{self.alert_count}"
            )

            sys.exit(0)

def main():

    monitor = LogMonitor(
        "logs/access.log",
        "output/alerts.log",
        replay_speed=2.0
    )

    monitor.run()

if __name__ == "__main__":
    main()
