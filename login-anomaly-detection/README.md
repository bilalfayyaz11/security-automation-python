# Login Anomaly Detection System

## What This Does

This implementation provides a Python-based login anomaly detection system that analyzes authentication activity from CSV logs and identifies suspicious user behavior.

The system builds baseline user profiles from successful login history, detects logins outside normal business hours, flags unusual login locations, and identifies high-frequency failed authentication attempts that may indicate brute-force activity.

This type of detection is useful for SOC teams, SIEM pipelines, security engineering workflows, DevSecOps automation, and AIOps-driven security monitoring.

## Architecture

    +-----------------------------+
    | Simulated Authentication    |
    | Data Generator              |
    | generate_logs.py            |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Authentication Dataset      |
    | auth_logs.csv               |
    | timestamp,user,ip,location  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Login Anomaly Engine        |
    | anomaly_detector.py         |
    | Pandas Data Processing      |
    | User Baseline Profiling     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Detection Layers            |
    | Time Anomaly Detection      |
    | Location Anomaly Detection  |
    | Failed Login Frequency      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Report             |
    | Suspicious Login Findings   |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- pandas

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install pandas

## How to Reproduce

Create the working directory:

mkdir -p ~/login-anomaly-detection

cd ~/login-anomaly-detection

Generate authentication data:

python3 generate_logs.py

Run anomaly detection:

python3 anomaly_detector.py

Verify generated files:

tree

Review generated authentication records:

head auth_logs.csv

## Tools Used

- Python 3
- pandas
- CSV
- Bash
- Linux
- Git
- tree

## Key Skills Demonstrated

- Security log analysis
- Authentication anomaly detection
- User behavior profiling
- Time-based anomaly detection
- Location-based anomaly detection
- Failed login frequency analysis
- Python data processing
- Pandas DataFrame operations
- SOC-style detection workflow design
- SIEM-style alert logic
- Cybersecurity automation
- AIOps security monitoring

## Real-World Use Case

Security teams use login anomaly detection to identify suspicious activity such as compromised accounts, impossible travel behavior, abnormal login times, unusual source locations, and brute-force attempts. In a production company, this logic could be integrated into a SIEM platform, cloud identity provider, endpoint monitoring pipeline, or internal security analytics system to help analysts prioritize risky authentication events.

## Lessons Learned

- Anomaly detection requires a clean baseline before suspicious behavior can be detected accurately.
- Using all successful logins as the baseline can accidentally hide rare suspicious locations.
- Failed authentication events should be separated from successful logins when detecting brute-force behavior.
- Time-based detection can be noisy if normal business hours are too strict.
- Combining multiple detection methods provides stronger coverage than relying on a single rule.

## Troubleshooting Log

Issue:
Global pip installation may fail on Ubuntu 24.04 because Python environments are externally managed.

Resolution:
Used a Python virtual environment before installing pandas.

Issue:
The original location anomaly logic did not flag Tokyo as suspicious.

Resolution:
Updated the baseline logic to use the most frequent known locations instead of accepting every successful login location as normal.

Issue:
The original frequency detection counted all login attempts.

Resolution:
Updated the detection logic to count only failed login attempts for brute-force-style behavior.

Issue:
The generated dataset produced many time-based anomalies because random timestamps included records before 8 AM.

Resolution:
Kept the output as valid detection behavior and documented that strict business-hour rules can create noisy alerts.

Issue:
tree may be missing in a fresh Ubuntu environment.

Resolution:
Installed tree through apt for clean file structure verification.
