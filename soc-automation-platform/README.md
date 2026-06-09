# SOC Automation Platform

## What This Does

This implementation provides a lightweight SOC automation platform that simulates security log ingestion, detects suspicious activity using signature-based rules, generates automated alerts, and produces a structured security report.

The platform includes a log generator, threat detection engine, alerting workflow, and report generator. It detects simulated brute force activity, port scans, suspicious outbound connections, and failed privilege escalation attempts.

This type of workflow is useful for SOC, Detection Engineering, Security Automation, DevSecOps, AIOps, and Blue Team environments where teams need faster visibility into suspicious activity.

## Architecture

    +-----------------------------+
    | Simulated Security Events   |
    | Normal + Suspicious Logs    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Log Generator               |
    | scripts/log_generator.py    |
    | logs/security.log           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Threat Detection Engine     |
    | scripts/threat_detector.py  |
    | Regex Threat Signatures     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Alert Output                |
    | alerts/threats.txt          |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Report Generator            |
    | scripts/report_generator.py |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Report             |
    | reports/security_report.txt |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- Basic Linux command-line knowledge
- Basic understanding of security logs and alerts

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/soc-lab/{logs,scripts,alerts,reports}

cd ~/soc-lab

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install watchdog

## How to Reproduce

Activate the Python environment:

source venv/bin/activate

Start the simulated security log generator:

python3 scripts/log_generator.py > /tmp/log_generator.out 2>&1 &

echo $! > /tmp/log_generator.pid

Start the threat detection engine:

python3 scripts/threat_detector.py > /tmp/threat_detector.out 2>&1 &

echo $! > /tmp/detector.pid

Allow the workflow to collect events:

sleep 60

Stop background processes:

kill $(cat /tmp/log_generator.pid) 2>/dev/null || true

kill $(cat /tmp/detector.pid) 2>/dev/null || true

Generate the security report:

python3 scripts/report_generator.py

Review generated logs:

head -20 logs/security.log

Review detected alerts:

cat alerts/threats.txt

Review final report:

cat reports/security_report.txt

Run Python syntax validation:

python3 -m py_compile scripts/log_generator.py scripts/threat_detector.py scripts/report_generator.py

## Tools Used

- Python 3
- Regex
- Bash
- Linux
- Python virtual environments
- watchdog
- Git
- tree

## Key Skills Demonstrated

- SOC workflow automation
- Security log generation
- Log ingestion and parsing
- Threat signature design
- Regex-based detection engineering
- Automated alert generation
- Security report generation
- Incident visibility workflow design
- Blue Team automation
- AIOps-style event processing
- Linux process management
- Python-based security tooling

## Real-World Use Case

Security operations teams monitor logs from servers, endpoints, firewalls, cloud platforms, and applications to detect suspicious activity. This platform demonstrates the same core workflow at a smaller scale: collect logs, apply detection rules, generate alerts, and summarize findings for analyst review. In production, this pattern maps to SIEM, SOAR, EDR, and cloud security monitoring pipelines.

## Lessons Learned

- Security visibility starts with structured log collection.
- Simple regex-based rules can detect common suspicious behaviors quickly.
- Detection logic must match the real log format exactly or alerts will be missed.
- Automated reporting helps analysts prioritize findings instead of manually reading raw logs.
- Background process handling is important when building continuous monitoring workflows.

## Troubleshooting Log

Issue:
The original package installation used global pip installation.

Resolution:
Used a Python virtual environment to avoid Ubuntu 24.04 externally managed Python environment issues.

Issue:
The original scripts contained incomplete TODO sections.

Resolution:
Implemented complete log generation, threat detection, alert writing, alert parsing, summary creation, and report generation logic.

Issue:
The threat detector needed to monitor newly appended log lines continuously.

Resolution:
Opened the log file, moved the cursor to the end, and continuously read new lines with a short sleep interval.

Issue:
Report generation could fail if the alert file did not exist.

Resolution:
Added alert file existence handling before parsing alerts.

Issue:
Fresh Ubuntu environments may not include tree.

Resolution:
Installed tree through apt for final structure verification.
EOFcd ~/soc-lab

cat > README.md << 'EOF'
# SOC Automation Platform

## What This Does

This implementation provides a lightweight SOC automation platform that simulates security log ingestion, detects suspicious activity using signature-based rules, generates automated alerts, and produces a structured security report.

The platform includes a log generator, threat detection engine, alerting workflow, and report generator. It detects simulated brute force activity, port scans, suspicious outbound connections, and failed privilege escalation attempts.

This type of workflow is useful for SOC, Detection Engineering, Security Automation, DevSecOps, AIOps, and Blue Team environments where teams need faster visibility into suspicious activity.

## Architecture

    +-----------------------------+
    | Simulated Security Events   |
    | Normal + Suspicious Logs    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Log Generator               |
    | scripts/log_generator.py    |
    | logs/security.log           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Threat Detection Engine     |
    | scripts/threat_detector.py  |
    | Regex Threat Signatures     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Alert Output                |
    | alerts/threats.txt          |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Report Generator            |
    | scripts/report_generator.py |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Report             |
    | reports/security_report.txt |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- Basic Linux command-line knowledge
- Basic understanding of security logs and alerts

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/soc-lab/{logs,scripts,alerts,reports}

cd ~/soc-lab

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install watchdog

## How to Reproduce

Activate the Python environment:

source venv/bin/activate

Start the simulated security log generator:

python3 scripts/log_generator.py > /tmp/log_generator.out 2>&1 &

echo $! > /tmp/log_generator.pid

Start the threat detection engine:

python3 scripts/threat_detector.py > /tmp/threat_detector.out 2>&1 &

echo $! > /tmp/detector.pid

Allow the workflow to collect events:

sleep 60

Stop background processes:

kill $(cat /tmp/log_generator.pid) 2>/dev/null || true

kill $(cat /tmp/detector.pid) 2>/dev/null || true

Generate the security report:

python3 scripts/report_generator.py

Review generated logs:

head -20 logs/security.log

Review detected alerts:

cat alerts/threats.txt

Review final report:

cat reports/security_report.txt

Run Python syntax validation:

python3 -m py_compile scripts/log_generator.py scripts/threat_detector.py scripts/report_generator.py

## Tools Used

- Python 3
- Regex
- Bash
- Linux
- Python virtual environments
- watchdog
- Git
- tree

## Key Skills Demonstrated

- SOC workflow automation
- Security log generation
- Log ingestion and parsing
- Threat signature design
- Regex-based detection engineering
- Automated alert generation
- Security report generation
- Incident visibility workflow design
- Blue Team automation
- AIOps-style event processing
- Linux process management
- Python-based security tooling

## Real-World Use Case

Security operations teams monitor logs from servers, endpoints, firewalls, cloud platforms, and applications to detect suspicious activity. This platform demonstrates the same core workflow at a smaller scale: collect logs, apply detection rules, generate alerts, and summarize findings for analyst review. In production, this pattern maps to SIEM, SOAR, EDR, and cloud security monitoring pipelines.

## Lessons Learned

- Security visibility starts with structured log collection.
- Simple regex-based rules can detect common suspicious behaviors quickly.
- Detection logic must match the real log format exactly or alerts will be missed.
- Automated reporting helps analysts prioritize findings instead of manually reading raw logs.
- Background process handling is important when building continuous monitoring workflows.

## Troubleshooting Log

Issue:
The original package installation used global pip installation.

Resolution:
Used a Python virtual environment to avoid Ubuntu 24.04 externally managed Python environment issues.

Issue:
The original scripts contained incomplete TODO sections.

Resolution:
Implemented complete log generation, threat detection, alert writing, alert parsing, summary creation, and report generation logic.

Issue:
The threat detector needed to monitor newly appended log lines continuously.

Resolution:
Opened the log file, moved the cursor to the end, and continuously read new lines with a short sleep interval.

Issue:
Report generation could fail if the alert file did not exist.

Resolution:
Added alert file existence handling before parsing alerts.

Issue:
Fresh Ubuntu environments may not include tree.

Resolution:
Installed tree through apt for final structure verification.
EOFcd ~/soc-lab

cat > README.md << 'EOF'
# SOC Automation Platform

## What This Does

This implementation provides a lightweight SOC automation platform that simulates security log ingestion, detects suspicious activity using signature-based rules, generates automated alerts, and produces a structured security report.

The platform includes a log generator, threat detection engine, alerting workflow, and report generator. It detects simulated brute force activity, port scans, suspicious outbound connections, and failed privilege escalation attempts.

This type of workflow is useful for SOC, Detection Engineering, Security Automation, DevSecOps, AIOps, and Blue Team environments where teams need faster visibility into suspicious activity.

## Architecture

    +-----------------------------+
    | Simulated Security Events   |
    | Normal + Suspicious Logs    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Log Generator               |
    | scripts/log_generator.py    |
    | logs/security.log           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Threat Detection Engine     |
    | scripts/threat_detector.py  |
    | Regex Threat Signatures     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Alert Output                |
    | alerts/threats.txt          |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Report Generator            |
    | scripts/report_generator.py |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Report             |
    | reports/security_report.txt |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- Basic Linux command-line knowledge
- Basic understanding of security logs and alerts

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/soc-lab/{logs,scripts,alerts,reports}

cd ~/soc-lab

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install watchdog

## How to Reproduce

Activate the Python environment:

source venv/bin/activate

Start the simulated security log generator:

python3 scripts/log_generator.py > /tmp/log_generator.out 2>&1 &

echo $! > /tmp/log_generator.pid

Start the threat detection engine:

python3 scripts/threat_detector.py > /tmp/threat_detector.out 2>&1 &

echo $! > /tmp/detector.pid

Allow the workflow to collect events:

sleep 60

Stop background processes:

kill $(cat /tmp/log_generator.pid) 2>/dev/null || true

kill $(cat /tmp/detector.pid) 2>/dev/null || true

Generate the security report:

python3 scripts/report_generator.py

Review generated logs:

head -20 logs/security.log

Review detected alerts:

cat alerts/threats.txt

Review final report:

cat reports/security_report.txt

Run Python syntax validation:

python3 -m py_compile scripts/log_generator.py scripts/threat_detector.py scripts/report_generator.py

## Tools Used

- Python 3
- Regex
- Bash
- Linux
- Python virtual environments
- watchdog
- Git
- tree

## Key Skills Demonstrated

- SOC workflow automation
- Security log generation
- Log ingestion and parsing
- Threat signature design
- Regex-based detection engineering
- Automated alert generation
- Security report generation
- Incident visibility workflow design
- Blue Team automation
- AIOps-style event processing
- Linux process management
- Python-based security tooling

## Real-World Use Case

Security operations teams monitor logs from servers, endpoints, firewalls, cloud platforms, and applications to detect suspicious activity. This platform demonstrates the same core workflow at a smaller scale: collect logs, apply detection rules, generate alerts, and summarize findings for analyst review. In production, this pattern maps to SIEM, SOAR, EDR, and cloud security monitoring pipelines.

## Lessons Learned

- Security visibility starts with structured log collection.
- Simple regex-based rules can detect common suspicious behaviors quickly.
- Detection logic must match the real log format exactly or alerts will be missed.
- Automated reporting helps analysts prioritize findings instead of manually reading raw logs.
- Background process handling is important when building continuous monitoring workflows.

## Troubleshooting Log

Issue:
The original package installation used global pip installation.

Resolution:
Used a Python virtual environment to avoid Ubuntu 24.04 externally managed Python environment issues.

Issue:
The original scripts contained incomplete TODO sections.

Resolution:
Implemented complete log generation, threat detection, alert writing, alert parsing, summary creation, and report generation logic.

Issue:
The threat detector needed to monitor newly appended log lines continuously.

Resolution:
Opened the log file, moved the cursor to the end, and continuously read new lines with a short sleep interval.

Issue:
Report generation could fail if the alert file did not exist.

Resolution:
Added alert file existence handling before parsing alerts.

Issue:
Fresh Ubuntu environments may not include tree.

Resolution:
Installed tree through apt for final structure verification.
EOFcd ~/soc-lab

cat > README.md << 'EOF'
# SOC Automation Platform

## What This Does

This implementation provides a lightweight SOC automation platform that simulates security log ingestion, detects suspicious activity using signature-based rules, generates automated alerts, and produces a structured security report.

The platform includes a log generator, threat detection engine, alerting workflow, and report generator. It detects simulated brute force activity, port scans, suspicious outbound connections, and failed privilege escalation attempts.

This type of workflow is useful for SOC, Detection Engineering, Security Automation, DevSecOps, AIOps, and Blue Team environments where teams need faster visibility into suspicious activity.

## Architecture

    +-----------------------------+
    | Simulated Security Events   |
    | Normal + Suspicious Logs    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Log Generator               |
    | scripts/log_generator.py    |
    | logs/security.log           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Threat Detection Engine     |
    | scripts/threat_detector.py  |
    | Regex Threat Signatures     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Alert Output                |
    | alerts/threats.txt          |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Report Generator            |
    | scripts/report_generator.py |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Report             |
    | reports/security_report.txt |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- Basic Linux command-line knowledge
- Basic understanding of security logs and alerts

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/soc-lab/{logs,scripts,alerts,reports}

cd ~/soc-lab

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install watchdog

## How to Reproduce

Activate the Python environment:

source venv/bin/activate

Start the simulated security log generator:

python3 scripts/log_generator.py > /tmp/log_generator.out 2>&1 &

echo $! > /tmp/log_generator.pid

Start the threat detection engine:

python3 scripts/threat_detector.py > /tmp/threat_detector.out 2>&1 &

echo $! > /tmp/detector.pid

Allow the workflow to collect events:

sleep 60

Stop background processes:

kill $(cat /tmp/log_generator.pid) 2>/dev/null || true

kill $(cat /tmp/detector.pid) 2>/dev/null || true

Generate the security report:

python3 scripts/report_generator.py

Review generated logs:

head -20 logs/security.log

Review detected alerts:

cat alerts/threats.txt

Review final report:

cat reports/security_report.txt

Run Python syntax validation:

python3 -m py_compile scripts/log_generator.py scripts/threat_detector.py scripts/report_generator.py

## Tools Used

- Python 3
- Regex
- Bash
- Linux
- Python virtual environments
- watchdog
- Git
- tree

## Key Skills Demonstrated

- SOC workflow automation
- Security log generation
- Log ingestion and parsing
- Threat signature design
- Regex-based detection engineering
- Automated alert generation
- Security report generation
- Incident visibility workflow design
- Blue Team automation
- AIOps-style event processing
- Linux process management
- Python-based security tooling

## Real-World Use Case

Security operations teams monitor logs from servers, endpoints, firewalls, cloud platforms, and applications to detect suspicious activity. This platform demonstrates the same core workflow at a smaller scale: collect logs, apply detection rules, generate alerts, and summarize findings for analyst review. In production, this pattern maps to SIEM, SOAR, EDR, and cloud security monitoring pipelines.

## Lessons Learned

- Security visibility starts with structured log collection.
- Simple regex-based rules can detect common suspicious behaviors quickly.
- Detection logic must match the real log format exactly or alerts will be missed.
- Automated reporting helps analysts prioritize findings instead of manually reading raw logs.
- Background process handling is important when building continuous monitoring workflows.

## Troubleshooting Log

Issue:
The original package installation used global pip installation.

Resolution:
Used a Python virtual environment to avoid Ubuntu 24.04 externally managed Python environment issues.

Issue:
The original scripts contained incomplete TODO sections.

Resolution:
Implemented complete log generation, threat detection, alert writing, alert parsing, summary creation, and report generation logic.

Issue:
The threat detector needed to monitor newly appended log lines continuously.

Resolution:
Opened the log file, moved the cursor to the end, and continuously read new lines with a short sleep interval.

Issue:
Report generation could fail if the alert file did not exist.

Resolution:
Added alert file existence handling before parsing alerts.

Issue:
Fresh Ubuntu environments may not include tree.

Resolution:
Installed tree through apt for final structure verification.
