# Policy Misconfiguration Detection Engine

## What This Does

This implementation provides a Python-based policy misconfiguration detection engine that analyzes firewall rules and access-control policies for insecure, conflicting, or overly permissive configurations.

The engine detects public network exposure, dangerous wildcard access, access to sensitive system resources, and conflicting firewall rules that could create operational or security gaps.

This type of automation supports Cloud Security, Network Security, DevSecOps, Governance/Risk/Compliance, and Security Engineering teams by turning policy files into actionable security findings.

## Architecture

    +-----------------------------+
    | Security Policy Inputs      |
    | firewall_policy.json        |
    | access_policy.json          |
    | secure_policy.json          |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | JSON Policy Loader          |
    | policy_detector.py          |
    | Syntax + File Validation    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Detection Engine            |
    | Overly Permissive Source    |
    | Conflicting Firewall Rules  |
    | Wildcard User Permissions   |
    | Sensitive Resource Access   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Findings Report    |
    | Critical Findings           |
    | High Findings               |
    | Conflict Findings           |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- JSON validation support through Python standard library

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/policy-misconfiguration-engine

cd ~/policy-misconfiguration-engine

## How to Reproduce

Validate the policy files:

python3 -m json.tool firewall_policy.json >/dev/null && echo "FIREWALL JSON VALID"

python3 -m json.tool access_policy.json >/dev/null && echo "ACCESS POLICY JSON VALID"

python3 -m json.tool secure_policy.json >/dev/null && echo "SECURE POLICY JSON VALID"

Run the detection engine:

python3 policy_detector.py

Test the secure policy case:

python3 - << 'PY'
from policy_detector import PolicyDetector
detector = PolicyDetector()
policy = detector.load_policy("secure_policy.json")
detector.analyze_firewall_policy(policy)
print("Findings:", len(detector.findings))
PY

Verify the final file structure:

tree

## Detection Rules Implemented

- Public SSH exposure from 0.0.0.0/0
- Public RDP exposure from 0.0.0.0/0
- Allow-all inbound traffic
- Conflicting firewall rules with different actions
- Wildcard user permissions
- Non-admin access to sensitive resources
- Guest access to restricted paths
- Everyone-readable security logs
- Secure-policy false-positive validation

## Tools Used

- Python 3
- JSON
- Bash
- Linux
- Git
- tree

## Key Skills Demonstrated

- Security policy analysis
- Firewall rule auditing
- Access-control review
- Misconfiguration detection
- Policy-as-code validation
- Conflict detection
- JSON parsing
- Compliance automation fundamentals
- Cloud security posture review
- Network security governance
- DevSecOps control validation
- Security engineering automation

## Real-World Use Case

Security teams use policy misconfiguration detection to identify exposed management ports, overly broad firewall rules, conflicting access controls, and unauthorized access to sensitive resources. In a real environment, this kind of engine could be integrated into CI/CD pipelines, cloud governance workflows, firewall change reviews, infrastructure-as-code checks, or compliance audits to prevent insecure configurations from reaching production.

## Lessons Learned

- Public source ranges such as 0.0.0.0/0 need careful review when paired with administrative ports.
- Conflicting allow and deny rules can create ambiguity depending on rule evaluation order.
- Wildcard users should almost never be granted access to sensitive resources.
- Security log files can contain sensitive forensic evidence and should not be broadly readable.
- Secure test cases are useful for proving that the engine does not produce false positives.

## Troubleshooting Log

Issue:
The original dependency instructions installed PyYAML even though the implementation only analyzes JSON files.

Resolution:
Kept the implementation JSON-native and documented that PyYAML is unnecessary for this version.

Issue:
Global pip package installation can be unreliable on Ubuntu 24.04 because of externally managed Python behavior.

Resolution:
Used system packages only for this implementation because no third-party Python dependency is required.

Issue:
Conflicting firewall rules were listed without an explicit severity label.

Resolution:
Tracked conflicts separately in the summary because rule conflicts can create policy ambiguity and bypass risk.

Issue:
JSON syntax mistakes can stop the detector from loading policies.

Resolution:
Validated policy files with python3 -m json.tool before running the detector.

Issue:
The secure policy test needed to confirm the engine does not flag valid configurations.

Resolution:
Added secure_policy.json and verified that it returns zero findings.
