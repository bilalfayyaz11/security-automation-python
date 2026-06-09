# Cloud Security Audit Engine

## What This Does

This implementation provides a security audit engine that analyzes infrastructure artifacts and security logs to identify configuration weaknesses, excessive permissions, insecure firewall exposure, authentication threats, and compliance violations.

The platform performs automated configuration analysis, log-based threat detection, compliance scoring, and HTML report generation. It combines multiple security assessment techniques into a single workflow that helps security teams quickly identify and prioritize remediation efforts.

This type of solution is useful for Cloud Security, DevSecOps, Security Engineering, Governance Risk and Compliance (GRC), Detection Engineering, and Security Operations teams responsible for maintaining secure infrastructure environments.

## Architecture

    +------------------------------+
    | Security Artifacts           |
    | SSH Configurations           |
    | Firewall Rules               |
    | User Permissions             |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Configuration Analyzer       |
    | audit_configs.py             |
    | SSH Review                   |
    | Firewall Analysis            |
    | Permission Auditing          |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Configuration Findings       |
    | config_audit.json            |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Security Logs                |
    | auth.log                     |
    | access.log                   |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Log Security Analyzer        |
    | audit_logs.py                |
    | Failed Login Detection       |
    | Brute Force Detection        |
    | Sensitive Access Detection   |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Log Findings                 |
    | log_audit.json               |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Compliance Engine            |
    | generate_report.py           |
    | Severity Scoring             |
    | Compliance Calculation       |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | HTML Compliance Report       |
    | compliance_report.html       |
    +------------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- jq
- curl
- Git
- tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv jq curl git tree

mkdir -p ~/security-audit-lab

cd ~/security-audit-lab

mkdir -p configs logs artifacts reports

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install pyyaml requests

## How to Reproduce

Activate the virtual environment:

source venv/bin/activate

Run configuration audit:

python3 audit_configs.py

Run log audit:

python3 audit_logs.py

Generate compliance report:

python3 generate_report.py

Review generated findings:

cat reports/config_audit.json

cat reports/log_audit.json

Review compliance report:

ls -lh reports/compliance_report.html

Validate JSON report counts:

jq '. | length' reports/config_audit.json

jq '. | length' reports/log_audit.json

Run syntax validation:

python3 -m py_compile audit_configs.py audit_logs.py generate_report.py

## Tools Used

- Python 3
- JSON
- YAML
- jq
- PyYAML
- requests
- Regex
- Bash
- Linux
- Git

## Key Skills Demonstrated

- Cloud security auditing
- Configuration assessment
- Firewall rule analysis
- SSH hardening review
- Identity and access auditing
- Log analysis
- Threat detection
- Compliance scoring
- Security reporting
- HTML report generation
- Security automation
- Risk prioritization
- Security governance controls

## Real-World Use Case

Organizations routinely assess cloud environments, virtual machines, firewall policies, access controls, and authentication activity to identify weaknesses before they are exploited. This audit engine demonstrates the same workflow by reviewing security artifacts and operational logs, producing findings, assigning risk levels, and generating compliance reports that can support security operations, cloud security reviews, and governance initiatives.

## Lessons Learned

- Security misconfigurations are often easier to identify through automated analysis than manual review.
- Excessive access permissions create unnecessary risk and should be reviewed regularly.
- Authentication logs provide valuable indicators of attack activity.
- Compliance scoring helps security teams prioritize remediation efforts.
- Automated reporting improves consistency and repeatability across security assessments.

## Troubleshooting Log

Issue:
Ubuntu 24.04 may restrict global Python package installation.

Resolution:
Created and used a Python virtual environment before installing dependencies.

Issue:
Configuration files may contain insecure defaults that are difficult to identify manually.

Resolution:
Implemented automated checks for root login, password authentication, firewall exposure, and password aging.

Issue:
Failed login attempts may not be obvious in large log files.

Resolution:
Implemented automated parsing and correlation of repeated authentication failures.

Issue:
Compliance scoring required consistent severity weighting.

Resolution:
Applied weighted scoring for CRITICAL, HIGH, MEDIUM, and LOW findings.

Issue:
HTML reporting required aggregation of findings from multiple audit modules.

Resolution:
Created a centralized report generator that combines configuration and log analysis results into a single compliance dashboard.
