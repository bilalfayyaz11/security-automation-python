# File Integrity Monitoring and Tamper Detection

## What This Does

This implementation provides a host-based file integrity monitoring system that detects unauthorized changes to critical files.

The system uses AIDE to create a trusted baseline of selected files, compare future filesystem states against that baseline, and report changes such as modified content, permission changes, deleted files, and newly added suspicious files.

An automated alert script captures AIDE findings into timestamped reports and a centralized alert log, making the workflow useful for security monitoring, incident response, compliance checks, and tamper detection.

## Architecture

    +-----------------------------+
    | Critical Files              |
    | /opt/critical_files         |
    | config.txt                  |
    | data.txt                    |
    | script.sh                   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | AIDE Configuration          |
    | /etc/aide/aide.conf         |
    | Custom Monitoring Rule      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Baseline Database           |
    | /var/lib/aide/aide.db       |
    | File Attributes + Hashes    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Integrity Check Engine      |
    | aide --check                |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Tamper Detection Report     |
    | /tmp/aide_report.txt        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Alert Automation            |
    | integrity_monitor.sh        |
    | /var/log/aide_alerts.log    |
    | /var/log/aide_check_*.log   |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- sudo access
- AIDE
- Bash
- tree
- coreutils
- Git

## Setup & Installation

sudo apt update

sudo apt install -y aide tree git coreutils

aide --version

tree --version

## How to Reproduce

Create the monitored directory and sample critical files:

sudo mkdir -p /opt/critical_files

sudo bash -c 'echo "Original content - Configuration file" > /opt/critical_files/config.txt'

sudo bash -c 'echo "Original content - Data file" > /opt/critical_files/data.txt'

sudo bash -c 'cat > /opt/critical_files/script.sh << SCRIPT
#!/bin/bash
echo "Critical maintenance script"
SCRIPT'

sudo chmod 755 /opt/critical_files/script.sh

Create a targeted AIDE configuration:

sudo tee /etc/aide/aide.conf > /dev/null << 'CONFIG'
database=file:/var/lib/aide/aide.db
database_out=file:/var/lib/aide/aide.db.new
gzip_dbout=no

R = p+i+n+u+g+s+m+c+sha256

/opt/critical_files R
CONFIG

Initialize the baseline database:

sudo aide --config=/etc/aide/aide.conf --init

sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db

Run a clean integrity check:

sudo aide --config=/etc/aide/aide.conf --check

Simulate file tampering:

sudo bash -c 'echo "TAMPERED - Malicious content added" >> /opt/critical_files/config.txt'

sudo chmod 777 /opt/critical_files/script.sh

sudo rm /opt/critical_files/data.txt

sudo bash -c 'echo "Backdoor script" > /opt/critical_files/backdoor.sh'

Generate a tamper detection report:

sudo aide --config=/etc/aide/aide.conf --check > /tmp/aide_report.txt 2>&1 || true

cat /tmp/aide_report.txt

Install the alert automation script:

sudo cp integrity_monitor.sh /usr/local/bin/integrity_monitor.sh

sudo chmod +x /usr/local/bin/integrity_monitor.sh

Run the monitoring script:

sudo /usr/local/bin/integrity_monitor.sh

View alerts:

sudo cat /var/log/aide_alerts.log

Restore the original file state:

sudo bash -c 'echo "Original content - Configuration file" > /opt/critical_files/config.txt'

sudo chmod 755 /opt/critical_files/script.sh

sudo bash -c 'echo "Original content - Data file" > /opt/critical_files/data.txt'

sudo rm -f /opt/critical_files/backdoor.sh

Update the trusted baseline:

sudo aide --config=/etc/aide/aide.conf --update

sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db

Run final clean verification:

sudo aide --config=/etc/aide/aide.conf --check

## Tools Used

- Linux
- AIDE
- Bash
- SHA-256
- coreutils
- tree
- Git

## Key Skills Demonstrated

- File integrity monitoring
- Host-based intrusion detection
- Tamper detection
- Baseline database creation
- Security alert automation
- Linux security monitoring
- Critical file monitoring
- Permission-change detection
- Unauthorized file detection
- Security report generation
- Incident response support workflows
- Compliance-oriented monitoring controls

## Real-World Use Case

A security team can use this workflow to monitor sensitive configuration files, application scripts, privileged binaries, and compliance-critical directories. If malware, a malicious insider, or an attacker modifies a protected file, changes permissions, removes evidence, or drops a backdoor script, AIDE can detect the change and produce an alert for investigation.

## Lessons Learned

- Full-system AIDE initialization can be slow on cloud training machines because it scans and hashes a very large number of files.
- A targeted AIDE configuration is faster, cleaner, and better for focused monitoring of critical paths.
- AIDE requires an activated baseline database before it can reliably detect changes.
- Integrity monitoring detects unauthorized changes, but alerting automation is needed to make the output operationally useful.
- File changes, permission changes, deleted files, and newly added files all represent different investigation signals.

## Troubleshooting Log

Issue:
The first full-system AIDE initialization took more than 20 minutes because the default Ubuntu configuration scanned a large system ruleset.

Resolution:
Verified the process was active using ps and CPU usage, then switched to a targeted monitoring configuration for /opt/critical_files to complete the workflow efficiently.

Issue:
The command aide --update failed with a missing configuration error.

Resolution:
Used explicit configuration syntax: aide --config=/etc/aide/aide.conf --update.

Issue:
The command ls -lh /var/lib/aide/ failed with permission denied.

Resolution:
Used sudo ls -lh /var/lib/aide/ because AIDE database files are protected.

Issue:
The SSH session disconnected during long-running initialization.

Resolution:
Checked process state, database files, and AIDE logs after reconnection before continuing.

Issue:
The original alert logic depended on version-specific wording.

Resolution:
Used a more reliable detection condition based on AIDE exit status and common report keywords such as added, removed, changed, and difference.
