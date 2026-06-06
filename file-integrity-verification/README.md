# File Integrity Verification Toolkit

## What This Does

This implementation provides a file integrity verification toolkit that generates, stores, and validates cryptographic checksums for monitored files.

The system uses SHA256 and MD5 hashing to establish a trusted baseline for file contents, then verifies files against that baseline to detect unauthorized modification, corruption, or tampering.

This type of verification is commonly used in cybersecurity, DevSecOps, backup validation, software distribution, compliance auditing, and server hardening workflows.

## Architecture

    +-------------------------------+
    | Monitored Files               |
    | original.txt                  |
    | document.txt                  |
    | test.txt                      |
    +---------------+---------------+
                    |
                    v
    +-------------------------------+
    | Hash Generation Layer         |
    | sha256sum                     |
    | md5sum                        |
    +---------------+---------------+
                    |
                    v
    +-------------------------------+
    | Trusted Checksum Baseline     |
    | original.sha256               |
    | original.md5                  |
    | all-files.sha256              |
    | checksums.sha256              |
    +---------------+---------------+
                    |
                    v
    +-------------------------------+
    | Integrity Verification Script |
    | integrity-checker.sh          |
    | generate mode                 |
    | verify mode                   |
    +---------------+---------------+
                    |
                    v
    +-------------------------------+
    | Verification Results          |
    | OK                            |
    | FAILED                        |
    | Tamper detection              |
    +-------------------------------+

## Prerequisites

- Ubuntu 24.04
- Bash
- coreutils
- sha256sum
- md5sum
- Git
- tree

## Setup & Installation

sudo apt update

sudo apt install -y coreutils tree git

mkdir -p ~/file-integrity-verification

cd ~/file-integrity-verification

## How to Reproduce

Create baseline test files:

echo "This is my original file content." > original.txt

echo "Important data for verification." > document.txt

Generate SHA256 checksum:

sha256sum original.txt > original.sha256

Generate MD5 checksum:

md5sum original.txt > original.md5

Generate checksums for all text files:

sha256sum *.txt > all-files.sha256

Verify a file against its checksum:

sha256sum -c original.sha256

Run the automated integrity checker:

./integrity-checker.sh generate .

./integrity-checker.sh verify

Test tamper detection:

echo "Modified" >> document.txt

./integrity-checker.sh verify

Validate script syntax:

bash -n integrity-checker.sh

Inspect project structure:

tree

## Tools Used

- Bash
- sha256sum
- md5sum
- coreutils
- find
- sort
- xargs
- Linux file system utilities
- Git
- tree

## Key Skills Demonstrated

- File integrity verification
- Checksum generation
- SHA256 hash validation
- MD5 hash generation
- Tamper detection
- Bash automation
- Linux file monitoring fundamentals
- Stable baseline generation
- Security verification workflows
- DevSecOps integrity controls
- Backup and artifact validation

## Real-World Use Case

Production teams use checksum verification to confirm that critical files have not been modified, corrupted, or tampered with. This is especially important for validating software downloads, monitoring configuration files, checking deployment artifacts, confirming backup integrity, and supporting compliance evidence. A tool like this can be extended into cron-based monitoring, deployment validation, or security alerting for sensitive server directories.

## Lessons Learned

- Checksums provide a reliable way to detect even tiny file changes.
- SHA256 is preferred over MD5 for stronger integrity assurance.
- A checksum baseline must be generated before verification can be meaningful.
- Intentional modification tests are useful for proving detection accuracy.
- Stable file ordering improves reproducibility when generating checksum databases.

## Troubleshooting Log

Issue:
A failed checksum verification returns a non-zero exit code.

Resolution:
Used `|| true` during intentional tamper tests so the workflow continues while still showing the expected failure.

Issue:
The original basic find command can generate file lists in inconsistent order.

Resolution:
Used `sort -z` with null-delimited file handling to create a stable checksum baseline.

Issue:
Checksum verification can fail when file paths differ from where the baseline was generated.

Resolution:
Generated and verified checksums from the same working directory using relative paths.

Issue:
MD5 is weaker than SHA256 for security-sensitive integrity checks.

Resolution:
Used MD5 only for demonstration and SHA256 as the primary verification mechanism.

Issue:
The fresh environment may not include tree.

Resolution:
Installed tree through apt for verification and clean project structure output.
