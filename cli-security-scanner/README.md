# CLI Security Scanner

## What This Does

This implementation provides a command-line security scanner that analyzes files and directories for common sensitive data exposure patterns. The scanner detects hardcoded passwords, API keys, private key headers, IPv4 addresses, and email addresses using structured regular expression rules.

The tool supports both single-file scanning and recursive directory scanning, making it useful for quick local security checks before code is committed or reviewed. Findings are grouped by issue type and include severity, file path, line number, matched value, and surrounding context.

This type of scanner is a practical foundation for DevSecOps workflows, source code security checks, lightweight secret detection, and automated security review pipelines.

## Architecture

    +------------------------------+
    | CLI Input                    |
    | -f file / -d directory       |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Argument Parser              |
    | argparse                     |
    | Input Validation             |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Scan Engine                  |
    | security_scanner.py          |
    | File Reader                  |
    | Directory Traversal          |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Detection Rules              |
    | Regex Pattern Matching       |
    | Passwords                    |
    | API Keys                     |
    | Private Keys                 |
    | IP Addresses                 |
    | Email Addresses              |
    +--------------+---------------+
                   |
                   v
    +------------------------------+
    | Terminal Report              |
    | Severity Summary             |
    | Findings by Type             |
    | File + Line Context          |
    +------------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3.12+
- Git
- tree
- Basic Linux shell access

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip git tree

mkdir -p ~/cli-security-scanner

cd ~/cli-security-scanner

## How to Reproduce

Display scanner help:

python3 security_scanner.py --help

Scan a single file:

python3 security_scanner.py -f test_config.txt

Scan a directory recursively:

python3 security_scanner.py -d ~/cli-security-scanner

Test error handling for a missing file:

python3 security_scanner.py -f nonexistent.txt

Test help output when no arguments are passed:

python3 security_scanner.py

Verify detection output:

python3 security_scanner.py -f test_config.txt

View repository structure:

tree -a .

## Detection Capabilities

- Hardcoded passwords and secret assignments
- API keys and access tokens
- Private key headers
- IPv4 addresses
- Email addresses
- Recursive directory scanning
- Severity-based reporting
- File path and line number reporting
- Context-aware terminal output

## Tools Used

- Python 3
- argparse
- os
- re
- sys
- collections.defaultdict
- Linux
- Bash
- Git
- tree

## Key Skills Demonstrated

- Command-line tool development
- Secure code scanning
- Secret detection fundamentals
- Regex-based security analysis
- CLI argument parsing
- Recursive file traversal
- Error handling
- Terminal report formatting
- DevSecOps automation
- Application security workflow design

## Real-World Use Case

Engineering teams need lightweight ways to detect secrets and sensitive data before code reaches shared repositories or CI/CD pipelines. A tool like this can be used locally by developers, by security engineers during review, or as a pre-commit and pipeline check to identify risky values such as hardcoded credentials, exposed API keys, private key material, internal IP addresses, and email addresses. In production environments, this concept extends into secret scanning platforms, source code security tooling, and DevSecOps guardrails.

## Lessons Learned

- argparse provides a clean way to build reliable command-line interfaces.
- Regex-based detection is useful for quick scanning but must be tuned to reduce false positives.
- Directory scanning requires ignoring noisy folders such as .git, virtual environments, and cache directories.
- Security reports become more useful when findings include severity, file path, line number, and context.
- Built-in Python modules are enough to create practical security automation tools without extra dependencies.

## Troubleshooting Log

Issue:
The original setup suggested installing argparse with pip.

Resolution:
Skipped pip installation because argparse is included in the Python 3 standard library.

Issue:
Fresh Ubuntu environment may not include tree.

Resolution:
Installed tree using apt.

Issue:
Scanning directories can accidentally include cache, dependency, or repository metadata folders.

Resolution:
Added ignored directories for __pycache__, .git, .venv, venv, and node_modules.

Issue:
Naive IPv4 regex can match invalid addresses such as 999.999.999.999.

Resolution:
Used a stricter IPv4 pattern that limits each octet to the valid 0-255 range.

Issue:
Python cache directories can appear after running scripts.

Resolution:
Removed __pycache__ directories before preparing the repository files.
