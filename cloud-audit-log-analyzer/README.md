# Cloud Audit Log Analyzer

## What This Does

This implementation provides a Python-based cloud audit log analyzer that reviews JSON-formatted cloud activity logs and identifies risky security behavior.

The analyzer detects sensitive administrative actions, insecure configuration changes, suspicious access attempts, unusual access times, external user activity, privileged user creation, and long-lived access key exposure.

This type of automation supports Cloud Security, SOC, DevSecOps, Detection Engineering, and Cloud Governance teams by turning raw audit logs into actionable security findings.

## Architecture

    +-----------------------------+
    | Cloud Audit Log Sources     |
    | AWS / Azure / GCP Style     |
    | sample_audit_logs.json      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | JSON Parsing Layer          |
    | audit_analyzer.py           |
    | Schema-Aware Log Loading    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Detection Engine            |
    | Risky Action Rules          |
    | Misconfiguration Patterns   |
    | Suspicious Activity Checks  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Findings           |
    | Severity Classification     |
    | User + Source IP Context    |
    | Resource + Action Details   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Report Output      |
    | sample_report.txt           |
    | test_report.txt             |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- colorama

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install colorama

## How to Reproduce

Create the working directory:

mkdir -p ~/cloud-audit-analyzer

cd ~/cloud-audit-analyzer

Validate the sample audit log JSON:

python3 -m json.tool sample_audit_logs.json >/dev/null && echo "JSON VALID"

Run the analyzer against the sample cloud audit log:

python3 audit_analyzer.py sample_audit_logs.json

Save the sample report:

python3 audit_analyzer.py sample_audit_logs.json | tee sample_report.txt

Run the analyzer against the custom test case:

python3 audit_analyzer.py test_logs.json

Save the custom test report:

python3 audit_analyzer.py test_logs.json | tee test_report.txt

Verify expected finding counts:

grep -E "Risky Actions Found|Misconfigurations Found|Suspicious Activities Found|Total Security Issues" sample_report.txt

Review the final file structure:

tree

## Detection Rules Implemented

- Risky administrative actions
- Encryption disabling
- Audit logging modification
- Backup deletion
- Access key creation
- MFA disabling
- Privileged user creation
- Open SSH exposure to the internet
- Public access patterns
- Non-expiring access keys
- Failed access attempts
- External or unknown user activity
- Unusual access time detection

## Tools Used

- Python 3
- JSON
- colorama
- Bash
- Linux
- Git
- tree

## Key Skills Demonstrated

- Cloud audit log analysis
- Cloud security monitoring
- JSON security event parsing
- Detection engineering
- Cloud governance automation
- Risky action classification
- Misconfiguration detection
- Suspicious activity analysis
- Severity-based reporting
- Security recommendation generation
- SOC-style investigation support
- DevSecOps security automation

## Real-World Use Case

Cloud security teams rely on audit logs such as AWS CloudTrail, Azure Activity Logs, and Google Cloud Audit Logs to detect unauthorized access, dangerous configuration changes, privileged identity activity, and control-plane abuse. This analyzer demonstrates how a security engineering team could build custom detection logic to identify risky administrative actions, insecure network changes, disabled controls, suspicious users, and policy violations before they become incidents.

## Lessons Learned

- Audit logs are one of the most important sources of cloud security evidence.
- JSON-formatted logs are easy to parse but require consistent field structures.
- Risky cloud actions need context such as user, source IP, resource, status, and timestamp.
- Expected lab findings can miss realistic risks such as administrator permissions and non-expiring keys.
- Detection rules become stronger when they combine action names, details fields, status values, and user identity patterns.

## Troubleshooting Log

Issue:
The original install command used pip3 install --user colorama.

Resolution:
Used a Python virtual environment because Ubuntu 24.04 can block or discourage global Python package installation through externally managed environment controls.

Issue:
The original expected output underestimated the number of security findings.

Resolution:
Expanded detection logic to identify additional realistic risks including privileged user creation, administrator permissions, non-expiring access keys, and suspicious time values inside the details field.

Issue:
Unusual access time detection only checked timestamps.

Resolution:
Added detection for time values embedded inside the details field, such as production database access at 02:30 AM.

Issue:
JSON syntax mistakes can break the analyzer.

Resolution:
Validated JSON files with python3 -m json.tool before running analysis.

Issue:
colorama may not be installed in a fresh environment.

Resolution:
The analyzer safely falls back to normal text output if colorama is unavailable.
