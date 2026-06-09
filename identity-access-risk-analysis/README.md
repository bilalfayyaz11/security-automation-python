# Identity and Access Risk Analysis Framework

## What This Does

This implementation provides an automated identity and access risk analysis framework that correlates user identity records, permission assignments, and behavior logs to calculate prioritized user risk scores.

The system analyzes privileged access, failed authentication attempts, after-hours activity, and sensitive actions such as configuration changes or record deletion. It produces a structured report that helps security teams identify high-risk users and investigate risky access patterns faster.

This type of automation is useful for IAM, SOC, GRC, Security Engineering, and AIOps teams that need to detect excessive privilege, suspicious activity, and potential insider-risk indicators across user populations.

## Architecture

    +-----------------------------+
    | Identity Records            |
    | data/users.json             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Permission Assignments      |
    | data/permissions.json       |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Behavior Logs               |
    | data/behavior_logs.json     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | IAM Risk Engine             |
    | scripts/iam_risk_analyzer.py|
    | Identity Correlation        |
    | Permission Risk Scoring     |
    | Behavior Risk Scoring       |
    | Composite Risk Calculation  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Risk Report                 |
    | reports/iam_risk_report.txt |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python virtual environments
- Python pip
- Git
- jq
- tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git jq tree

mkdir -p ~/iam-risk-lab/{data,scripts,reports}

cd ~/iam-risk-lab

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install pandas numpy

## How to Reproduce

Activate the Python environment:

source venv/bin/activate

Run the IAM risk analyzer:

python3 scripts/iam_risk_analyzer.py

View the generated report:

cat reports/iam_risk_report.txt

Validate JSON input files:

jq . data/users.json

jq . data/permissions.json

jq . data/behavior_logs.json

Check generated risk levels:

grep "Risk Level:" reports/iam_risk_report.txt

Identify high-risk users:

grep -A 2 "Risk Level: HIGH" reports/iam_risk_report.txt

Test individual user analysis:

python3 << 'PYTHON'
import sys
sys.path.append("scripts")
from iam_risk_analyzer import IAMRiskAnalyzer

analyzer = IAMRiskAnalyzer(
    "data/users.json",
    "data/permissions.json",
    "data/behavior_logs.json"
)

result = analyzer.calculate_composite_risk("U003")

print("User U003 Risk Analysis:")
print(f"  Composite Risk: {result['composite_risk']}")
print(f"  Risk Level: {result['risk_level']}")
PYTHON

## Tools Used

- Python 3
- JSON
- jq
- Bash
- Linux
- Git
- tree
- Python virtual environments

## Key Skills Demonstrated

- Identity and access risk analysis
- IAM data correlation
- Permission risk scoring
- Behavioral risk analysis
- Failed authentication detection
- After-hours activity detection
- High-risk action classification
- Composite risk modeling
- Security report generation
- Python automation for cybersecurity workflows
- SOC and IAM investigation support
- Least-privilege assessment

## Real-World Use Case

Security teams need a reliable way to identify users who have both sensitive permissions and suspicious behavior patterns. In a real company, this framework could be connected to IAM platforms, authentication logs, cloud audit logs, SIEM events, and HR identity records to prioritize investigations around excessive privileges, compromised accounts, insider-risk indicators, and least-privilege violations.

## Lessons Learned

- IAM risk becomes more useful when identity, access, and behavior data are analyzed together.
- Admin permissions carry higher operational risk and should be weighted more heavily.
- Failed login attempts and after-hours activity can increase behavioral risk.
- Composite scoring helps prioritize security investigations instead of reviewing users manually.
- Python is effective for building lightweight security analytics workflows from structured JSON data.

## Troubleshooting Log

Issue:
Global pip installation can fail on Ubuntu 24.04 because Python is externally managed.

Resolution:
Created and used a Python virtual environment before installing Python dependencies.

Issue:
The original dependency list included pandas even though the script did not require DataFrame processing.

Resolution:
Kept the dependency available for future analytics extensions, but wrote the core analyzer using standard Python libraries.

Issue:
Timestamp parsing based only on string splitting can fail if a malformed timestamp is introduced.

Resolution:
Used datetime parsing with exception handling to make behavior analysis more reliable.

Issue:
The original working directory name was not suitable for a professional portfolio structure.

Resolution:
Kept the local execution directory unchanged, but prepared the portfolio folder as identity-access-risk-analysis.

Issue:
Risk analysis needed persistent output for review.

Resolution:
Generated reports/iam_risk_report.txt as a reusable text artifact.
