#!/usr/bin/env python3

import re
import json
from collections import defaultdict

def analyze_auth_logs(log_file):
    findings = []
    failed_attempts = defaultdict(int)

    with open(log_file, "r") as f:
        for line in f:
            if "Failed login attempt" in line:
                ip_match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
                if ip_match:
                    failed_attempts[ip_match.group(1)] += 1

            if "Brute force attack" in line:
                findings.append({"severity": "CRITICAL", "type": "Brute Force Attack", "details": line.strip()})

    for ip, count in failed_attempts.items():
        if count >= 2:
            findings.append({"severity": "HIGH", "type": "Multiple Failed Logins", "details": f"IP {ip} had {count} failed login attempts"})

    return findings

def analyze_access_logs(log_file):
    findings = []

    with open(log_file, "r") as f:
        for line in f:
            if "403" in line:
                findings.append({"severity": "MEDIUM", "type": "Unauthorized Access Attempt", "details": line.strip()})

            if "/admin/" in line or "/api/secrets" in line:
                findings.append({"severity": "MEDIUM", "type": "Sensitive Endpoint Access", "details": line.strip()})

            if "DELETE" in line:
                findings.append({"severity": "LOW", "type": "Delete Operation", "details": line.strip()})

    return findings

def main():
    all_findings = []
    all_findings.extend(analyze_auth_logs("logs/auth.log"))
    all_findings.extend(analyze_access_logs("logs/access.log"))

    print(f"Total Security Events: {len(all_findings)}")
    for finding in all_findings:
        print(f"[{finding['severity']}] {finding['type']}")

    with open("reports/log_audit.json", "w") as f:
        json.dump(all_findings, f, indent=2)

if __name__ == "__main__":
    main()
