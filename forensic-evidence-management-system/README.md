# Forensic Evidence Management System

## What This Does

This implementation provides a secure forensic evidence collection and reporting workflow for preserving digital artifacts during incident response and investigation activities.

The system collects simulated evidence, preserves original files in a protected read-only state, generates MD5 and SHA256 hashes, creates working copies for analysis, documents chain of custody, verifies integrity, and produces structured forensic reports.

This workflow is useful for Digital Forensics, Incident Response, SOC, Blue Team, Security Operations, and Cybersecurity Analyst roles where evidence integrity and documentation are critical.

## Architecture

    +-----------------------------+
    | Source Evidence             |
    | suspicious_doc.txt          |
    | system.log                  |
    | app.conf                    |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Forensic Collection         |
    | dcfldd                      |
    | MD5 + SHA256 Hashing        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Protected Evidence Store    |
    | evidence/original           |
    | Read-Only Permissions       |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Working Analysis Copies     |
    | evidence/working            |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Integrity Artifacts         |
    | evidence/hashes             |
    | Hash Manifests              |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Custody Documentation       |
    | chain_of_custody.log        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Reporting Layer             |
    | generate_report.py          |
    | forensic_report.txt         |
    | executive_summary.txt       |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- dcfldd
- hashdeep / md5deep
- Python 3
- Python pip
- tree
- Bash
- Basic understanding of file permissions and cryptographic hashes

## Setup & Installation

sudo apt update

sudo apt install -y dcfldd hashdeep python3 python3-pip tree

mkdir -p ~/forensics_lab

cd ~/forensics_lab

mkdir -p evidence/{original,working,reports}

mkdir -p evidence/logs

mkdir -p evidence/hashes

chmod 755 evidence

chmod 700 evidence/original

chmod 755 evidence/working

chmod 755 evidence/reports

## How to Reproduce

Create sample evidence files:

cat > suspicious_doc.txt << 'DATA'
Confidential Project Data - Access Log
User: jdoe - Access Time: 2024-01-15 14:23:45
Action: Downloaded sensitive files
DATA

cat > system.log << 'DATA'
2024-01-15 14:20:12 LOGIN jdoe from 192.168.1.105
2024-01-15 14:23:45 FILE_ACCESS jdoe accessed /secure/data.db
2024-01-15 14:24:01 FILE_DOWNLOAD jdoe downloaded data.db
2024-01-15 14:25:33 LOGOUT jdoe
DATA

cat > app.conf << 'DATA'
[database]
host=192.168.1.50
user=admin
last_modified=2024-01-15
DATA

Collect evidence using dcfldd:

dcfldd if=suspicious_doc.txt of=evidence/original/suspicious_doc.txt hash=md5,sha256 hashlog=evidence/hashes/suspicious_doc.hash

dcfldd if=system.log of=evidence/original/system.log hash=md5,sha256 hashlog=evidence/hashes/system.log.hash

dcfldd if=app.conf of=evidence/original/app.conf hash=md5,sha256 hashlog=evidence/hashes/app.conf.hash

Protect original evidence:

chmod 444 evidence/original/*

Create working copies:

cp -p evidence/original/* evidence/working/

Generate hash manifests:

cd evidence/original

md5deep -r . > ../hashes/md5_manifest.txt

sha256sum * > ../hashes/sha256_manifest.txt

Return to the main directory:

cd ~/forensics_lab

Generate forensic report:

python3 generate_report.py

Verify evidence integrity:

./verify_integrity.sh

Review generated reports:

cat evidence/reports/forensic_report.txt

cat evidence/reports/executive_summary.txt

Review chain of custody:

cat evidence/logs/chain_of_custody.log

Run syntax validation:

python3 -m py_compile generate_report.py

## Tools Used

- dcfldd
- hashdeep
- md5deep
- sha256sum
- Python 3
- hashlib
- Bash
- Linux permissions
- tree

## Key Skills Demonstrated

- Digital forensic evidence collection
- Chain of custody documentation
- Evidence integrity verification
- Cryptographic hashing
- MD5 and SHA256 checksum generation
- Read-only evidence preservation
- Working-copy analysis workflow
- Automated forensic report generation
- Incident response evidence handling
- Secure file permission management
- Bash automation
- Python-based reporting

## Real-World Use Case

During security incidents, investigators must collect files, logs, and configuration artifacts without altering the original evidence. This workflow demonstrates how evidence can be collected, hashed, protected, documented, and reported in a repeatable way that supports incident response, internal investigations, and forensic review.

## Lessons Learned

- Original evidence should be protected immediately after collection.
- Hashes provide a reliable way to prove evidence integrity.
- Working copies allow analysis without modifying preserved originals.
- Chain of custody documentation is essential for investigation credibility.
- Automated reporting reduces manual errors and improves consistency.

## Troubleshooting Log

Issue:
The original tool list referenced md5deep directly.

Resolution:
Installed hashdeep, which provides md5deep-compatible functionality on Ubuntu 24.04.

Issue:
Original evidence can be accidentally modified if permissions are not restricted.

Resolution:
Changed original evidence files to read-only permissions using chmod 444.

Issue:
Hash verification can fail if original evidence is modified after manifest creation.

Resolution:
Generated SHA256 manifest after collection and used sha256sum -c for verification.

Issue:
Large files should not be read entirely into memory during hashing.

Resolution:
The Python report generator reads files in chunks when calculating hashes.

Issue:
Chain of custody must include timestamps, sizes, and cryptographic hashes.

Resolution:
Generated a chain of custody log with item name, collection time, size, and SHA256 value.
