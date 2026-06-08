# Event Alert Response Processing Pipeline

## What This Does

This implementation provides an event-driven security processing pipeline that ingests security event logs, applies YAML-based detection rules, generates structured alert files, and records simulated automated response actions. It models the core workflow used in SOC automation, SIEM detection pipelines, and SOAR-style response systems.

The pipeline supports threshold-based detection for repeated failed logins, suspicious file access, port scans, and privilege escalation attempts. It produces JSON alert artifacts, response logs, and a pipeline summary containing event counts, alert counts, response counts, severity distribution, and response action statistics.

This type of automation helps Security Operations, Detection Engineering, Incident Response, DevSecOps, and Cybersecurity Automation teams convert raw logs into actionable security events.

## Architecture

    +-----------------------------+
    | Security Event Log           |
    | logs/security_events.log     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Event Processor              |
    | event_processor.py           |
    | - Parses events              |
    | - Loads YAML rules           |
    | - Counts event thresholds    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Detection Rules              |
    | rules/security_rules.yaml    |
    | - FAILED_LOGIN               |
    | - UNAUTHORIZED_ACCESS        |
    | - PORT_SCAN                  |
    | - PRIVILEGE_ESCALATION       |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Alert and Response Layer     |
    | alerts/*.json                |
    | responses/*.json             |
    | output/pipeline_summary      |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python virtual environments
- PyYAML
- tree
- Git

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv tree git

mkdir -p ~/event-alert-response-pipeline/{logs,rules,alerts,responses,output}

cd ~/event-alert-response-pipeline

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

pip install pyyaml

## How to Reproduce

Generate sample security events:

venv/bin/python generate_events.py

Process the event log once:

venv/bin/python event_processor.py --mode once

View raw events:

cat logs/security_events.log

Review generated alerts:

ls -lh alerts/

python3 -m json.tool "$(ls alerts/*.json | head -1)"

Review generated responses:

ls -lh responses/

python3 -m json.tool "$(ls responses/*.json | head -1)"

Review the pipeline summary:

python3 -m json.tool output/pipeline_summary.json

Add a manual failed-login sequence:

echo "$(date '+%Y-%m-%d %H:%M:%S') | 203.0.113.50 | FAILED_LOGIN | User: test" >> logs/security_events.log

echo "$(date '+%Y-%m-%d %H:%M:%S') | 203.0.113.50 | FAILED_LOGIN | User: test" >> logs/security_events.log

echo "$(date '+%Y-%m-%d %H:%M:%S') | 203.0.113.50 | FAILED_LOGIN | User: test" >> logs/security_events.log

Reprocess events with a custom summary file:

rm -f alerts/*.json responses/*.json output/pipeline_summary_custom.json

venv/bin/python event_processor.py --mode once --summary output/pipeline_summary_custom.json

Review the custom summary:

python3 -m json.tool output/pipeline_summary_custom.json

Optional monitor mode:

venv/bin/python event_processor.py --mode monitor

Verify Python syntax:

venv/bin/python -m py_compile event_processor.py generate_events.py

Review file tree:

tree .

## Tools Used

- Python 3
- PyYAML
- YAML
- JSON
- argparse
- collections.Counter
- defaultdict
- pathlib
- Bash
- Linux
- tree
- Git

## Key Skills Demonstrated

- Event-driven security workflow design
- Rule-based threat detection
- YAML-driven detection configuration
- Threshold-based alerting
- Security event parsing
- Structured alert generation
- Automated response simulation
- SOAR-style response workflows
- SIEM-style event processing
- SOC automation fundamentals
- Detection engineering logic
- Incident response artifact generation
- JSON reporting for downstream automation

## Real-World Use Case

A SOC team can use this type of pipeline to process events from authentication logs, EDR alerts, firewall logs, cloud audit logs, or application security telemetry. For example, repeated failed logins from the same source IP can trigger an alert and simulated IP block, unauthorized access to sensitive files can trigger an administrator alert, and repeated port-scan events can be logged for investigation. In production, similar logic can feed SIEM dashboards, SOAR playbooks, ticketing systems, notification channels, and firewall automation.

## Lessons Learned

- Threshold-based rules help reduce noise by alerting only when repeated behavior crosses a defined limit.
- YAML makes detection rules easier to modify without changing Python code.
- Alert filenames need sufficient uniqueness to avoid overwriting files generated within the same second.
- Deterministic batch processing is useful for testing before implementing live monitoring.
- Summary reports make pipeline output easier to review, validate, and integrate with other tools.

## Troubleshooting Log

Issue:
The original workflow included watchdog as a dependency but did not use it in the implementation.

Resolution:
Removed the unused dependency and implemented deterministic once mode plus optional polling-based monitor mode.

Issue:
The original alert filename used only rule ID and integer seconds, which can overwrite multiple alerts generated in the same second.

Resolution:
Added source IP and millisecond timestamp to alert and response filenames.

Issue:
The original implementation generated alerts and responses but did not produce a pipeline-level summary.

Resolution:
Added output/pipeline_summary.json with events processed, alerts generated, responses executed, severity counts, response counts, alert details, and response details.

Issue:
The original rules did not include privilege escalation detection.

Resolution:
Added a PRIVILEGE_ESCALATION rule with simulated host isolation response.

Issue:
Global pip installation can fail or create dependency hygiene issues on Ubuntu 24.04.

Resolution:
Created a Python virtual environment and installed PyYAML inside the isolated environment.
