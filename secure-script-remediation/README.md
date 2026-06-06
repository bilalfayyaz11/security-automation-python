# Secure Script Remediation

## What This Does

This implementation demonstrates a complete security remediation workflow for flawed Python and Bash scripts. It identifies authentication bypass, command injection, hardcoded secrets, unsafe file handling, missing input validation, and weak Bash scripting practices, then replaces them with secure and maintainable implementations.

The Python remediation hardens a user management script by fixing authentication logic, replacing unsafe shell execution, hashing password comparisons, validating user input, and adding reliable file handling. The Bash remediation improves a backup script using strict error handling, quoted variables, safe directory checks, secure logging, and ShellCheck validation.

This project reflects real-world secure code review work performed by DevSecOps, Application Security, Platform Engineering, and Security Automation teams when hardening internal tools before production use.

## Architecture

    +----------------------------------+
    | Flawed Scripts                   |
    | user_manager.py                  |
    | backup_script.sh                 |
    +----------------+-----------------+
                     |
                     v
    +----------------------------------+
    | Security Review Layer            |
    | Authentication Logic Review      |
    | Command Injection Review         |
    | Secret Exposure Review           |
    | File Handling Review             |
    | ShellCheck Static Analysis       |
    +----------------+-----------------+
                     |
                     v
    +----------------------------------+
    | Remediation Layer                |
    | user_manager_fixed.py            |
    | backup_script_fixed.sh           |
    +----------------+-----------------+
                     |
          +----------+----------+
          |                     |
          v                     v
    +------------------+   +------------------+
    | Python Hardening |   | Bash Hardening   |
    | Hash Comparison  |   | set -euo pipefail|
    | subprocess.run   |   | Quoted Variables |
    | Input Validation |   | Directory Checks |
    | Context Managers |   | Safe Logging     |
    +---------+--------+   +---------+--------+
              |                      |
              +----------+-----------+
                         |
                         v
    +----------------------------------+
    | Verification Tests               |
    | Auth Bypass Test                 |
    | Injection Prevention Test        |
    | Invalid Input Test               |
    | ShellCheck Test                  |
    | Backup Success/Error Tests       |
    +----------------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Bash
- shellcheck
- Git
- tree
- Basic Linux shell access

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip shellcheck tree git

mkdir -p ~/secure-script-remediation

cd ~/secure-script-remediation

## How to Reproduce

Run the secure Python authentication test:

echo -e "1\nadmin\nwrong" | python3 user_manager_fixed.py

Expected result:

Access denied

Run username validation test:

echo -e "3\nuser@123" | python3 user_manager_fixed.py

Expected result:

Invalid username. Use 3-20 alphanumeric characters.

Run safe system user listing:

echo -e "2" | python3 user_manager_fixed.py

Run ShellCheck against the hardened Bash script:

shellcheck backup_script_fixed.sh

Create backup test data:

mkdir -p ~/test_backup

echo "test file" > ~/test_backup/test.txt

Run successful backup:

./backup_script_fixed.sh ~/test_backup

Verify backup output:

ls -la /tmp/backups

cat /tmp/backups/backup.log

Test error handling:

./backup_script_fixed.sh /nonexistent/directory

View repository structure:

tree -a .

## Tools Used

- Python 3
- Bash
- hashlib
- subprocess
- ShellCheck
- Linux
- Git
- tree

## Key Skills Demonstrated

- Secure code review
- Vulnerability remediation
- Authentication bypass prevention
- Command injection mitigation
- Secret removal from scripts
- Defensive Python programming
- Defensive Bash scripting
- Input validation
- Static analysis with ShellCheck
- Error handling
- File handling improvements
- Production script hardening

## Real-World Use Case

Internal automation scripts are frequently created quickly by engineering, operations, or security teams and later become part of production workflows. If these scripts contain authentication flaws, command injection risks, hardcoded secrets, or unsafe Bash practices, they can become serious operational and security liabilities. This remediation workflow mirrors how DevSecOps and Application Security teams review existing internal tools, identify vulnerabilities, apply secure fixes, validate behavior, and document the remediation path before allowing scripts into production environments.

## Lessons Learned

- Small logic mistakes such as using OR instead of AND can create complete authentication bypasses.
- User-controlled input should never be concatenated into shell commands.
- subprocess.run with argument lists is safer than os.system for command execution.
- Bash scripts should quote variables and use strict mode to reduce unsafe runtime behavior.
- ShellCheck is valuable for catching common Bash reliability and security issues.
- Secure remediation requires both fixing code and proving the fix with targeted tests.

## Troubleshooting Log

Issue:
The original Python script stored a plaintext admin password directly in code.

Resolution:
Replaced direct password comparison with SHA-256 hash comparison.

Issue:
The original authentication logic used OR instead of AND.

Resolution:
Changed authentication to require both the correct username and matching password hash.

Issue:
The original Python script used os.system with user-controlled input.

Resolution:
Replaced shell command concatenation with subprocess.run using a fixed argument list.

Issue:
The original user writing function did not validate input and did not append newlines.

Resolution:
Added username validation and newline-separated file writes.

Issue:
The original file operations did not use context managers.

Resolution:
Replaced manual open and close operations with with statements.

Issue:
The original Bash script used unquoted variables.

Resolution:
Quoted all variable expansions to prevent word splitting and unsafe path handling.

Issue:
The original Bash script had no input validation.

Resolution:
Added argument count validation and source directory existence checks.

Issue:
The original Bash script included a hardcoded password in the log output.

Resolution:
Removed secret output and replaced it with safe operational logging.

Issue:
The original Bash script lacked reliable runtime safety controls.

Resolution:
Added set -euo pipefail and explicit error handling.

Issue:
Python cache directories can appear after script execution.

Resolution:
Removed __pycache__ directories before repository preparation.
