#!/usr/bin/env python3

import json
import sys
from collections import defaultdict
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False

RISKY_ACTIONS = [
    "DisableEncryption",
    "ModifyLogging",
    "DeleteBackup",
    "CreateAccessKey",
    "DisableMFA",
    "CreateUser"
]

MISCONFIGURATION_PATTERNS = {
    "open_ssh": "0.0.0.0/0 on port 22",
    "open_rdp": "0.0.0.0/0 on port 3389",
    "public_access": "public-read",
    "no_encryption": "encryption: false",
    "admin_permissions": "Administrator",
    "non_expiring_key": "never"
}

def color(text, severity):
    if not COLORS_AVAILABLE:
        return text

    if severity == "CRITICAL":
        return Fore.RED + text + Style.RESET_ALL

    if severity == "HIGH":
        return Fore.YELLOW + text + Style.RESET_ALL

    if severity == "MEDIUM":
        return Fore.CYAN + text + Style.RESET_ALL

    return text

def load_audit_logs(filename):
    try:
        with open(filename, "r") as f:
            logs = json.load(f)

        print(f"[+] Loaded {len(logs)} log entries from {filename}")

        return logs

    except FileNotFoundError:
        print(f"[!] Error: File '{filename}' not found")
        sys.exit(1)

    except json.JSONDecodeError:
        print(f"[!] Error: Invalid JSON format in '{filename}'")
        sys.exit(1)

def analyze_risky_actions(logs):
    findings = []

    for log in logs:
        action = log.get("action", "")

        if action in RISKY_ACTIONS:
            findings.append({
                "severity": "HIGH",
                "type": "Risky Action",
                "timestamp": log.get("timestamp"),
                "user": log.get("user"),
                "action": action,
                "resource": log.get("resource"),
                "source_ip": log.get("source_ip"),
                "details": log.get("details", {})
            })

    return findings

def detect_misconfigurations(logs):
    findings = []

    for log in logs:
        details_str = json.dumps(log.get("details", {}))

        for config_name, pattern in MISCONFIGURATION_PATTERNS.items():
            if pattern in details_str:
                findings.append({
                    "severity": "CRITICAL",
                    "type": "Misconfiguration",
                    "timestamp": log.get("timestamp"),
                    "user": log.get("user"),
                    "action": log.get("action"),
                    "issue": config_name.replace("_", " ").title(),
                    "resource": log.get("resource"),
                    "source_ip": log.get("source_ip"),
                    "details": log.get("details", {})
                })

    return findings

def detect_suspicious_activity(logs):
    findings = []

    for log in logs:
        if log.get("status") == "FAILED":
            findings.append({
                "severity": "MEDIUM",
                "type": "Suspicious Activity",
                "timestamp": log.get("timestamp"),
                "user": log.get("user"),
                "action": log.get("action"),
                "issue": "Failed Access Attempt",
                "source_ip": log.get("source_ip"),
                "details": log.get("details", {})
            })

        timestamp = log.get("timestamp", "")
        details = log.get("details", {})

        details_time = str(details.get("time", ""))

        if (
            "T02:" in timestamp or
            "T03:" in timestamp or
            "T04:" in timestamp or
            "02:" in details_time or
            "03:" in details_time or
            "04:" in details_time
        ):
            findings.append({
                "severity": "MEDIUM",
                "type": "Suspicious Activity",
                "timestamp": timestamp,
                "user": log.get("user"),
                "action": log.get("action"),
                "issue": "Unusual Access Time",
                "source_ip": log.get("source_ip"),
                "details": log.get("details", {})
            })

        user = log.get("user", "")

        if "external" in user or "unknown" in user:
            findings.append({
                "severity": "HIGH",
                "type": "Suspicious Activity",
                "timestamp": log.get("timestamp"),
                "user": user,
                "action": log.get("action"),
                "issue": "External User Activity",
                "source_ip": log.get("source_ip"),
                "details": log.get("details", {})
            })

    return findings

def generate_report(logs, risky_actions, misconfigs, suspicious):
    print("\n" + "=" * 70)
    print("           CLOUD AUDIT LOG SECURITY ANALYSIS REPORT")
    print("=" * 70)

    print("\n[SUMMARY]")
    print(f"Total Log Entries Analyzed: {len(logs)}")
    print(f"Risky Actions Found: {len(risky_actions)}")
    print(f"Misconfigurations Found: {len(misconfigs)}")
    print(f"Suspicious Activities Found: {len(suspicious)}")

    total_issues = len(risky_actions) + len(misconfigs) + len(suspicious)

    print(f"\nTotal Security Issues: {total_issues}")

    severity_counts = defaultdict(int)

    for finding in risky_actions + misconfigs + suspicious:
        severity_counts[finding["severity"]] += 1

    print("\n[SEVERITY BREAKDOWN]")
    for severity in ["CRITICAL", "HIGH", "MEDIUM"]:
        print(f"{severity}: {severity_counts[severity]}")

    if risky_actions:
        print(f"\n{'=' * 70}")
        print("[RISKY ACTIONS DETECTED]")
        print("=" * 70)

        for idx, finding in enumerate(risky_actions, 1):
            print(color(f"\n{idx}. {finding['action']}", finding["severity"]))
            print(f"   Severity: {finding['severity']}")
            print(f"   User: {finding['user']}")
            print(f"   Source IP: {finding['source_ip']}")
            print(f"   Time: {finding['timestamp']}")
            print(f"   Resource: {finding['resource']}")
            print(f"   Details: {finding['details']}")

    if misconfigs:
        print(f"\n{'=' * 70}")
        print("[SECURITY MISCONFIGURATIONS]")
        print("=" * 70)

        for idx, finding in enumerate(misconfigs, 1):
            print(color(f"\n{idx}. {finding['issue']}", finding["severity"]))
            print(f"   Severity: {finding['severity']}")
            print(f"   User: {finding['user']}")
            print(f"   Action: {finding['action']}")
            print(f"   Resource: {finding['resource']}")
            print(f"   Source IP: {finding['source_ip']}")
            print(f"   Time: {finding['timestamp']}")
            print(f"   Details: {finding['details']}")

    if suspicious:
        print(f"\n{'=' * 70}")
        print("[SUSPICIOUS ACTIVITIES]")
        print("=" * 70)

        for idx, finding in enumerate(suspicious, 1):
            print(color(f"\n{idx}. {finding['issue']}", finding["severity"]))
            print(f"   Severity: {finding['severity']}")
            print(f"   User: {finding['user']}")
            print(f"   Action: {finding['action']}")
            print(f"   Time: {finding['timestamp']}")
            print(f"   Source IP: {finding['source_ip']}")
            print(f"   Details: {finding['details']}")

    print(f"\n{'=' * 70}")
    print("[RECOMMENDATIONS]")
    print("=" * 70)

    if misconfigs:
        print("- Restrict public security group access to trusted IP ranges only")
        print("- Remove administrator permissions from default or newly created users")
        print("- Enforce key expiration policies and rotate long-lived access keys")
        print("- Enable encryption for all storage resources")

    if risky_actions:
        print("- Require approval workflows for sensitive cloud administration actions")
        print("- Enable MFA for privileged accounts")
        print("- Review backup deletion, audit logging, and encryption changes")
        print("- Monitor IAM access key creation and privileged user provisioning")

    if suspicious:
        print("- Investigate failed access attempts from external users")
        print("- Review access from unknown source IP addresses")
        print("- Investigate unusual access time activity")
        print("- Correlate suspicious events with identity provider and network logs")

    print("\n" + "=" * 70 + "\n")

def main():
    print("\n=== Cloud Audit Log Analyzer ===\n")

    if len(sys.argv) < 2:
        print("Usage: python3 audit_analyzer.py <log_file.json>")
        print("Example: python3 audit_analyzer.py sample_audit_logs.json")
        sys.exit(1)

    log_file = sys.argv[1]

    logs = load_audit_logs(log_file)

    print("\n[*] Analyzing logs for security issues...")

    risky_actions = analyze_risky_actions(logs)
    misconfigs = detect_misconfigurations(logs)
    suspicious = detect_suspicious_activity(logs)

    generate_report(
        logs,
        risky_actions,
        misconfigs,
        suspicious
    )

if __name__ == "__main__":
    main()
