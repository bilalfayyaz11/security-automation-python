#!/usr/bin/env python3

def analyze_alerts(alert_file):

    try:

        with open(
            alert_file,
            'r'
        ) as f:

            lines = f.readlines()

        error_count = 0
        critical_count = 0

        for line in lines:

            if 'ERROR:' in line:
                error_count += 1

            elif 'CRITICAL:' in line:
                critical_count += 1

        print("=" * 50)
        print("ALERT STATISTICS")
        print("=" * 50)
        print(
            f"Total Alerts: "
            f"{len(lines)}"
        )
        print(
            f"ERROR Alerts: "
            f"{error_count}"
        )
        print(
            f"CRITICAL Alerts: "
            f"{critical_count}"
        )
        print("=" * 50)

    except FileNotFoundError:

        print(
            f"Alert file not found: "
            f"{alert_file}"
        )

if __name__ == "__main__":

    analyze_alerts(
        "output/alerts.log"
    )
