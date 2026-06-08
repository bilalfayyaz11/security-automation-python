# Linux Forensic Evidence Collector

## What This Does

This implementation provides an automated Linux forensic evidence collection workflow for incident response and security investigations. It collects host metadata, operating system details, user activity, process state, network configuration, system logs, authentication logs, kernel logs, and journal records into a timestamped evidence directory.

The collector generates MD5 and SHA256 hash manifests to support evidence integrity verification and includes a separate verification utility for validating collected artifacts after capture. It also creates compressed evidence archives with archive-level SHA256 verification so the collected package can be preserved or transferred with tamper-detection.

This type of automation helps SOC, DFIR, Platform Security, Cloud Security, and DevSecOps teams perform consistent first-response evidence capture across Linux systems.

## Architecture

    +----------------------------------+
    | Linux Host                       |
    | Ubuntu / Cloud VM / Server       |
    +----------------+-----------------+
                     |
                     v
    +----------------------------------+
    | Evidence Collection Script       |
    | collect_evidence.sh              |
    | - Host metadata                  |
    | - User/process state             |
    | - Network state                  |
    | - System logs                    |
    +----------------+-----------------+
                     |
                     v
    +----------------------------------+
    | Timestamped Evidence Directory   |
    | ~/evidence-collection/evidence_* |
    | - case_info.txt                  |
    | - logs/                          |
    | - system files                   |
    | - network files                  |
    +----------------+-----------------+
                     |
                     v
    +----------------------------------+
    | Integrity Layer                  |
    | - evidence_md5.txt               |
    | - evidence_sha256.txt            |
    | - archive SHA256 hash            |
    +----------------+-----------------+
                     |
                     v
    +----------------------------------+
    | Verification Utility             |
    | verify_evidence.sh               |
    | md5sum -c / sha256sum -c         |
    +----------------------------------+

## Prerequisites

- Ubuntu 24.04
- Bash
- sudo access
- coreutils
- util-linux
- iproute2
- net-tools
- tar
- tree
- Git

## Setup & Installation

sudo apt update

sudo apt install -y coreutils util-linux iproute2 net-tools tar tree git

mkdir -p ~/forensic-tools

mkdir -p ~/evidence-collection

cd ~/forensic-tools

chmod +x collect_evidence.sh verify_evidence.sh

## How to Reproduce

Run the evidence collector while preserving the original user home directory:

sudo HOME=/home/ubuntu ./collect_evidence.sh

Identify the latest evidence directory:

LATEST_EVIDENCE="$(find ~/evidence-collection -maxdepth 1 -type d -name 'evidence_*' | sort | tail -1)"

Verify collected evidence integrity:

./verify_evidence.sh "$LATEST_EVIDENCE"

Create a compressed evidence archive:

cd ~/evidence-collection

LATEST_EVIDENCE_DIR="$(find . -maxdepth 1 -type d -name 'evidence_*' | sort | tail -1 | sed 's#^\./##')"

tar -czf "${LATEST_EVIDENCE_DIR}_archive.tar.gz" "$LATEST_EVIDENCE_DIR"

sha256sum "${LATEST_EVIDENCE_DIR}_archive.tar.gz" > "${LATEST_EVIDENCE_DIR}_archive.sha256"

sha256sum -c "${LATEST_EVIDENCE_DIR}_archive.sha256"

Set evidence files to read-only:

chmod -R a-w "$LATEST_EVIDENCE_DIR"

Review evidence contents:

tree "$LATEST_EVIDENCE_DIR"

cat "$LATEST_EVIDENCE_DIR/case_info.txt"

cat "$LATEST_EVIDENCE_DIR/collection_summary.txt"

## Tools Used

- Bash
- Linux
- Ubuntu 24.04
- sudo
- coreutils
- md5sum
- sha256sum
- iproute2
- ss
- net-tools
- tar
- journalctl
- tree
- Git

## Key Skills Demonstrated

- Linux incident response automation
- Digital forensic evidence collection
- Bash scripting with strict execution controls
- Timestamped evidence storage
- Chain-of-custody metadata generation
- System log collection
- Authentication log collection
- Kernel and journal log preservation
- Network state capture
- Process and user activity capture
- Cryptographic integrity verification
- Archive creation and validation
- Defensive security automation
- SOC and DFIR workflow engineering

## Real-World Use Case

A security team can use this type of collector during the first stage of a Linux incident investigation to capture volatile and semi-volatile system data before it changes. For example, when a cloud VM is suspected of compromise, responders can run the collector to preserve active processes, logged-in users, network listeners, routing information, authentication logs, system logs, and journal records before containment or remediation begins. The generated hash manifests and archive hash provide integrity checks that help prove the evidence package has not been modified after collection.

## Lessons Learned

- Running collection scripts with sudo can change the effective home directory to /root unless HOME is explicitly preserved.
- Directory matching must avoid broad patterns that accidentally match archive files or hash files.
- ss is the preferred network socket inspection tool on modern Linux systems, while netstat should be treated as a fallback.
- Evidence verification is safer when the directory path is passed as an argument instead of being hardcoded inside the script.
- Evidence archives should not be pushed to GitHub because they may contain sensitive system logs and host metadata.

## Troubleshooting Log

Issue:
The first evidence verification attempt failed because no evidence directory appeared under /home/ubuntu/evidence-collection.

Resolution:
The script was executed with sudo, which changed the effective HOME path. The collector was rerun with HOME explicitly preserved using sudo HOME=/home/ubuntu ./collect_evidence.sh.

Issue:
The collector name appeared as Bilal_Fayyaz_root because whoami returned root during sudo execution.

Resolution:
This was documented as a sudo context issue. A production version should use SUDO_USER when available to preserve the original operator identity.

Issue:
The latest evidence detection command matched evidence_20260608_185251_archive.sha256 instead of the actual evidence directory.

Resolution:
Replaced broad shell glob matching with a directory-only find command:
find ~/evidence-collection -maxdepth 1 -type d -name 'evidence_*' | sort | tail -1

Issue:
The original workflow relied on netstat as the main network connection command.

Resolution:
Updated the collection logic to prefer ss -tuln and only fall back to netstat if ss is unavailable.

Issue:
The starter verification script used an empty hardcoded EVIDENCE_DIR variable.

Resolution:
Replaced the hardcoded variable with a command-line argument so any timestamped evidence directory can be verified safely.
