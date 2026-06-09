# Identity and Access Risk Scoring System

## What This Does

This implementation provides a Python-based Identity and Access Management risk scoring system that evaluates user accounts based on permissions, behavior patterns, and account hygiene.

The system generates synthetic IAM activity data, calculates permission risk, behavior risk, and password hygiene risk, assigns a total risk score to every user, and produces a ranked risk report for security review.

It also includes statistical anomaly detection to identify unusual login behavior, failed login patterns, off-hours access, and privilege escalation attempts.

## Architecture

    +-----------------------------+
    | IAM Data Generator          |
    | generate_data.py            |
    | Users, Roles, Activity      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | IAM Dataset                 |
    | iam_data.json               |
    | Permissions + Behavior      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Risk Scoring Engine         |
    | risk_scorer.py              |
    | Permission Risk             |
    | Behavior Risk               |
    | Account Hygiene Risk        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Risk Report Output          |
    | risk_report.csv             |
    | Ranked User Risk Scores     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Anomaly Detection Layer     |
    | anomaly_detector.py         |
    | Statistical Baselines       |
    | Suspicious Activity Flags   |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- pandas
- numpy

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install pandas numpy

## How to Reproduce

Create the working directory:

mkdir -p ~/identity-access-risk-scoring

cd ~/identity-access-risk-scoring

Generate IAM activity data:

python3 generate_data.py

Review generated IAM data:

cat iam_data.json

Run IAM risk scoring:

python3 risk_scorer.py

Review the CSV report:

cat risk_report.csv

Run anomaly detection:

python3 anomaly_detector.py

Add a high-risk test user:

python3 << 'PY'
import json

with open("iam_data.json", "r") as f:
    users = json.load(f)

users.append({
    "username": "test_user",
    "role": "admin",
    "department": "Test",
    "permissions": ["admin", "sudo", "delete", "config_change"],
    "activity": {
        "login_count": 80,
        "failed_logins": 25,
        "off_hours_access": 35,
        "data_downloads": 45,
        "privilege_escalation_attempts": 3
    },
    "last_password_change": 200
})

with open("iam_data.json", "w") as f:
    json.dump(users, f, indent=2)
PY

Re-run risk scoring after adding the high-risk test user:

python3 risk_scorer.py

View the highest-risk users:

python3 - << 'PY'
import pandas as pd
df = pd.read_csv("risk_report.csv")
print(df.sort_values("total_risk_score", ascending=False).head(5))
PY

Verify final structure:

tree

## Risk Factors Implemented

- High-risk permissions
- Medium-risk permissions
- Failed login activity
- Off-hours access behavior
- Privilege escalation attempts
- Excessive data downloads
- Password age
- Total risk scoring from 0 to 100
- Risk levels: LOW, MEDIUM, HIGH, CRITICAL
- Statistical anomaly detection using standard deviation thresholds

## Tools Used

- Python 3
- pandas
- numpy
- JSON
- CSV
- statistics module
- Bash
- Linux
- Git
- tree

## Key Skills Demonstrated

- IAM security analytics
- Identity risk scoring
- User behavior analysis
- Permission risk modeling
- Account hygiene assessment
- Insider-threat signal detection
- Statistical anomaly detection
- Security report generation
- CSV reporting with pandas
- JSON data processing
- Governance and access review automation
- SOC-style identity investigation support
- DevSecOps security analytics

## Real-World Use Case

Security teams use IAM risk scoring to identify accounts that combine risky permissions, suspicious behavior, and weak account hygiene. In an enterprise environment, this type of system could ingest identity provider logs, cloud IAM data, authentication events, and privilege activity to prioritize high-risk users for review, access removal, password rotation, MFA enforcement, or incident investigation.

## Lessons Learned

- IAM risk is stronger when multiple signals are combined instead of relying on a single indicator.
- Privileged users are not automatically malicious, but elevated permissions increase blast radius.
- Failed logins, off-hours access, and privilege escalation attempts are useful behavioral risk signals.
- Password age is a simple but important account hygiene factor.
- Small datasets make statistical anomaly detection less reliable than larger historical baselines.

## Troubleshooting Log

Issue:
The original install command used global pip installation for pandas and numpy.

Resolution:
Used a Python virtual environment because Ubuntu 24.04 can enforce externally managed Python package behavior.

Issue:
The generated data is random, so risk scores may vary between executions.

Resolution:
Validated results by reviewing risk distribution and adding a deterministic high-risk test user.

Issue:
Anomaly detection based on mean plus two standard deviations may be weak with only five users.

Resolution:
Documented the limitation and used the detector as a baseline demonstration of statistical anomaly detection.

Issue:
The risk scoring report needs a structured output for review.

Resolution:
Saved results to risk_report.csv using pandas.

Issue:
High-risk behavior needed explicit validation.

Resolution:
Added a test user with administrator permissions, failed logins, off-hours access, high downloads, privilege escalation attempts, and stale password age.
