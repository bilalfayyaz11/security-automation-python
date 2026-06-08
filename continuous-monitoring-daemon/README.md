# Continuous Monitoring Daemon with Log Replay

## What This Does

This implementation provides a Python-based monitoring daemon that replays historical log data, detects important operational events, generates alerts, and stores monitoring output for later analysis.

The system reads structured application-style logs, parses each entry, identifies ERROR and CRITICAL events, writes alert records to an output file, and provides a statistics analyzer to summarize generated alerts.

This type of workflow is useful for SRE, DevOps, Platform Engineering, SOC Operations, infrastructure monitoring, and AIOps teams that need automated visibility into system failures and critical events.

## Architecture

    +-----------------------------+
    | Historical Log Dataset      |
    | logs/access.log             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Log Replay Engine           |
    | monitor_daemon.py           |
    | Timed Event Playback        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Monitoring Logic            |
    | Parse Log Level             |
    | Detect ERROR / CRITICAL     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Alert Output Layer          |
    | output/alerts.log           |
    | output/daemon.log           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Alert Statistics Analyzer   |
    | analyze_alerts.py           |
    | ERROR / CRITICAL Counts     |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Git
- tree
- Basic Linux process management knowledge

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/continuous-monitoring-daemon

cd ~/continuous-monitoring-daemon

mkdir -p logs output

## How to Reproduce

Run the monitoring daemon in the foreground:

python3 monitor_daemon.py

Run the daemon in the background with nohup:

nohup python3 monitor_daemon.py > output/daemon.log 2>&1 &

echo $! > output/daemon.pid

Check daemon output:

tail -f output/daemon.log

View generated alerts:

cat output/alerts.log

Analyze alert statistics:

python3 analyze_alerts.py

Stop the background process if still running:

if [ -f output/daemon.pid ]; then kill $(cat output/daemon.pid) 2>/dev/null; fi

Verify final file structure:

tree

## Monitoring Rules Implemented

- INFO entries are replayed and displayed without alerting.
- WARNING entries are displayed but not escalated.
- ERROR entries trigger alert generation.
- CRITICAL entries trigger alert generation.
- Alerts are written to a persistent output file.
- Alert statistics are calculated from generated alert records.

## Tools Used

- Python 3
- Bash
- Linux
- nohup
- ps
- tail
- tree
- Git

## Key Skills Demonstrated

- Continuous monitoring design
- Log parsing and replay simulation
- Background process execution
- Daemon-style runtime behavior
- Alert generation
- Operational event classification
- Linux process management
- File-based monitoring output
- Infrastructure monitoring fundamentals
- AIOps-style event processing
- SRE diagnostic automation

## Real-World Use Case

Production engineering teams use monitoring daemons and log processors to detect application failures, infrastructure degradation, authentication issues, service outages, and critical system events. A more advanced version of this system could monitor live application logs, forward alerts into a SIEM or observability platform, and trigger notifications through Slack, PagerDuty, Jira, email, or incident response workflows.

## Lessons Learned

- Log replay is useful for testing monitoring logic before connecting to live production logs.
- ERROR and CRITICAL levels provide a simple but effective starting point for alerting.
- Background execution with nohup helps simulate daemon-style service behavior.
- A script that replays a fixed file exits naturally after processing all records.
- A true continuous daemon would keep tailing a log file instead of stopping after replay completion.

## Troubleshooting Log

Issue:
The monitoring script was described as continuous, but the implementation reads a fixed log file once and exits.

Resolution:
Documented the actual behavior as a log replay daemon and noted that true continuous monitoring would require a persistent tail loop.

Issue:
The background process may disappear quickly after being started with nohup.

Resolution:
Confirmed this is expected because the script completes after replaying all 15 log entries.

Issue:
No alerts may appear if the output directory does not exist.

Resolution:
Created the output directory before running the monitor.

Issue:
The expected alert count can increase if the script is run multiple times without clearing output/alerts.log.

Resolution:
Review or clear output/alerts.log before repeat testing when exact alert counts are required.

Issue:
tree may be missing in a fresh Ubuntu environment.

Resolution:
Installed tree through apt for clean file structure verification.
