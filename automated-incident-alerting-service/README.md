# Automated Incident Alerting Service

## What This Does

This implementation provides a real-time security incident alerting service that monitors log files, detects suspicious activity using configurable detection rules, and generates structured incident alerts.

The system reads security events from a live log file, matches each event against YAML-based alert rules, applies threshold logic, and sends notifications to both console output and a persistent incident log.

This type of automation is commonly used in SOC monitoring pipelines, SIEM workflows, DevSecOps alerting, security engineering platforms, and incident response systems.

## Architecture

    +-----------------------------+
    | Security Event Source       |
    | logs/security.log           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Real-Time Monitor           |
    | integrated_system.py        |
    | File Tail Logic             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Detection Rules             |
    | config/alert_config.yaml    |
    | Pattern + Severity + Limit  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Incident Decision Engine    |
    | Regex Matching              |
    | Threshold Counting          |
    | Rule Evaluation             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Alert Formatter             |
    | alert_formatter.py          |
    | Timestamp + Severity        |
    | Matched Log Evidence        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Notification Outputs        |
    | Console Alert               |
    | alerts/incidents.log        |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- PyYAML
- watchdog

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install pyyaml watchdog

## How to Reproduce

Create the working directory:

mkdir -p ~/incident-alerting-service

cd ~/incident-alerting-service

Create runtime directories:

mkdir -p logs alerts config

touch logs/security.log

Validate YAML configuration:

python3 -c "import yaml; yaml.safe_load(open('config/alert_config.yaml')); print('YAML VALID')"

Start the incident monitor in one terminal:

source venv/bin/activate

python3 integrated_system.py

Generate security events in a second terminal:

cd ~/incident-alerting-service

source venv/bin/activate

python3 generate_test_logs.py

Review generated incidents:

cat alerts/incidents.log

Verify the final structure:

tree

## Detection Rules Implemented

- Failed login attempts after repeated password failures
- Root access detection
- Port scan detection
- Rule severity classification
- Threshold-based incident triggering
- Console and file-based alert delivery

## Tools Used

- Python 3
- PyYAML
- watchdog
- Regex
- YAML
- Bash
- Linux
- Git
- tree

## Key Skills Demonstrated

- Real-time log monitoring
- Security incident detection
- YAML-driven rule configuration
- Regex-based event matching
- Threshold-based alert logic
- SOC-style alert generation
- SIEM workflow fundamentals
- Incident response automation
- Python security scripting
- Linux log processing
- DevSecOps monitoring automation
- Detection engineering foundations

## Real-World Use Case

Security teams use incident alerting services to detect suspicious events such as repeated failed logins, privileged access, scanning activity, and abnormal authentication behavior. In a production environment, this service could be connected to Linux authentication logs, cloud audit logs, firewall logs, or application security logs, then integrated with Slack, email, PagerDuty, Jira, Microsoft Teams, or a SIEM platform for rapid incident response.

## Lessons Learned

- YAML configuration makes detection rules easier to update without editing Python code.
- Thresholds reduce noisy alerts by requiring repeated suspicious activity before triggering.
- Regex matching provides flexible detection but requires careful pattern design.
- Alert output should include evidence, severity, timestamp, and rule context.
- Real-time monitoring needs predictable file handling and reliable log flushing.

## Troubleshooting Log

Issue:
Direct global pip installation may fail on Ubuntu 24.04 because Python environments are externally managed.

Resolution:
Used a Python virtual environment before installing PyYAML and watchdog.

Issue:
The original workflow introduced a separate incident monitor file but the functional detection workflow was implemented through the integrated system.

Resolution:
Used integrated_system.py as the main runtime service and kept the architecture focused on the working detection pipeline.

Issue:
Alerts may not appear if the monitor starts after logs are already written.

Resolution:
Started the monitor first, then generated test logs from a second terminal.

Issue:
Generated logs may not appear immediately if file writes are buffered.

Resolution:
Added f.flush() after each test event write in generate_test_logs.py.

Issue:
The alerts directory may not exist before the first alert is written.

Resolution:
Added directory creation logic inside alert_formatter.py before writing alerts.

Issue:
tree may be missing in a fresh Ubuntu environment.

Resolution:
Installed tree through apt for clean structure verification.
