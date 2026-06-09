#!/usr/bin/env python3

import json
import yaml

def analyze_ssh_config(config_file):
    findings = []
    with open(config_file, "r") as f:
        content = f.read()

    if "PermitRootLogin yes" in content:
        findings.append({"severity": "HIGH", "issue": "Root login is enabled", "recommendation": "Set PermitRootLogin to no"})

    if "PasswordAuthentication yes" in content:
        findings.append({"severity": "MEDIUM", "issue": "Password authentication enabled", "recommendation": "Use key-based authentication only"})

    if "MaxAuthTries 6" in content or "MaxAuthTries" not in content:
        findings.append({"severity": "MEDIUM", "issue": "MaxAuthTries is too high or not set", "recommendation": "Set MaxAuthTries to 3"})

    return findings

def analyze_firewall_rules(config_file):
    findings = []
    with open(config_file, "r") as f:
        config = json.load(f)

    for rule in config.get("rules", []):
        if rule.get("source") == "0.0.0.0/0":
            findings.append({"severity": "HIGH", "issue": f"Rule {rule['id']} allows access from anywhere", "recommendation": f"Restrict source IP for port {rule['port']}"})

    return findings

def analyze_user_permissions(config_file):
    findings = []
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    for user in config.get("users", []):
        if user.get("password_age", 0) > 90:
            findings.append({"severity": "MEDIUM", "issue": f"User {user['username']} has password age > 90 days", "recommendation": "Enforce 90-day password rotation"})

        if user.get("sudo") and user["username"] != "admin":
            findings.append({"severity": "LOW", "issue": f"User {user['username']} has sudo privileges", "recommendation": "Review if sudo access is necessary"})

    return findings

def main():
    all_findings = []
    all_findings.extend(analyze_ssh_config("configs/sshd_config.sample"))
    all_findings.extend(analyze_firewall_rules("configs/firewall_rules.json"))
    all_findings.extend(analyze_user_permissions("configs/users.yaml"))

    print(f"Total Findings: {len(all_findings)}")
    for finding in all_findings:
        print(f"[{finding['severity']}] {finding['issue']}")

    with open("reports/config_audit.json", "w") as f:
        json.dump(all_findings, f, indent=2)

if __name__ == "__main__":
    main()
