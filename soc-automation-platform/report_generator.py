#!/usr/bin/env python3

from datetime import datetime
from collections import Counter
import os


def parse_alerts(alert_file):
    threats = []

    if not os.path.exists(alert_file):
        return threats

    with open(alert_file, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split("|")
            timestamp = parts[0].strip()

            threat_type = "unknown"

            for part in parts:
                part = part.strip()
                if part.startswith("THREAT="):
                    threat_type = part.replace("THREAT=", "").strip()

            threats.append({
                "timestamp": timestamp,
                "threat_type": threat_type,
                "raw_alert": line
            })

    return threats


def generate_summary(threats):
    total = len(threats)
    threat_counts = Counter(threat["threat_type"] for threat in threats)

    breakdown = {}

    for threat_type, count in threat_counts.items():
        percentage = round((count / total) * 100, 2) if total > 0 else 0

        breakdown[threat_type] = {
            "count": count,
            "percentage": percentage
        }

    summary = {
        "total_threats": total,
        "threat_breakdown": breakdown,
        "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return summary


def create_report(summary, output_file):
    with open(output_file, "w") as report:
        report.write("=" * 70 + "\n")
        report.write("SOC AUTOMATION SECURITY REPORT\n")
        report.write("=" * 70 + "\n")
        report.write(f"Report Generated: {summary['report_time']}\n")
        report.write(f"Total Threats Detected: {summary['total_threats']}\n\n")

        report.write("Threat Breakdown:\n")
        report.write("-" * 70 + "\n")

        if not summary["threat_breakdown"]:
            report.write("No threats detected.\n")
        else:
            for threat_type, data in summary["threat_breakdown"].items():
                report.write(
                    f"- {threat_type}: {data['count']} detections "
                    f"({data['percentage']}%)\n"
                )

        report.write("\nRecommendations:\n")
        report.write("-" * 70 + "\n")

        if "brute_force" in summary["threat_breakdown"]:
            report.write("- Review failed admin login attempts and enforce account lockout controls.\n")

        if "port_scan" in summary["threat_breakdown"]:
            report.write("- Investigate scanning source IPs and validate firewall exposure.\n")

        if "suspicious_connection" in summary["threat_breakdown"]:
            report.write("- Investigate outbound connections to uncommon ports such as 4444.\n")

        if "privilege_escalation" in summary["threat_breakdown"]:
            report.write("- Review sudo activity and audit privilege escalation attempts.\n")

        if not summary["threat_breakdown"]:
            report.write("- Continue monitoring logs for suspicious activity.\n")


def main():
    alert_file = "alerts/threats.txt"
    report_file = "reports/security_report.txt"

    print("Generating security report...")

    threats = parse_alerts(alert_file)
    summary = generate_summary(threats)
    create_report(summary, report_file)

    print(f"Report saved to {report_file}")


if __name__ == "__main__":
    main()
