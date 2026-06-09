# Secure Code Hardening for AI-Generated Python

## What This Does

This implementation demonstrates how insecure AI-generated Python code can be reviewed, scanned, and hardened using secure coding practices.

The system includes vulnerable examples for SQL injection, path traversal, and command injection, then provides secure refactored versions using parameterized SQL queries, path validation, safe subprocess execution, and input validation.

Static analysis with Bandit is used to identify security weaknesses and compare vulnerable code against hardened implementations.

## Architecture

    +-----------------------------+
    | Insecure Python Examples    |
    | user_login.py               |
    | file_reader.py              |
    | command_executor.py         |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Static Security Analysis    |
    | Bandit SAST Scan            |
    | bandit_report.txt           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Secure Refactoring Layer    |
    | Parameterized Queries       |
    | Path Validation             |
    | Safe Subprocess Execution   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Hardened Python Code        |
    | user_login_secure.py        |
    | file_reader_secure.py       |
    | command_executor_secure.py  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Verification Workflow       |
    | Bandit Rescan               |
    | Functional Security Tests   |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python pip
- Python virtual environments
- Git
- tree
- Bandit
- Safety
- Pylint

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/secure-code-hardening

cd ~/secure-code-hardening

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install bandit safety pylint

## How to Reproduce

Activate the virtual environment:

source venv/bin/activate

Run the initial security scan against vulnerable code:

bandit -r . -f txt -o bandit_report.txt

Review detected findings:

cat bandit_report.txt

Scan the hardened code:

bandit user_login_secure.py file_reader_secure.py command_executor_secure.py -f txt

Compare vulnerable and hardened findings:

grep "Issue:" bandit_report.txt | wc -l

bandit user_login_secure.py file_reader_secure.py command_executor_secure.py 2>&1 | grep "Issue:" | wc -l

Create a safe file-read test environment:

mkdir -p /tmp/uploads

echo "test content" > /tmp/uploads/valid.txt

Test valid file access:

echo "valid.txt" | python3 file_reader_secure.py

Test path traversal handling:

echo "../../etc/passwd" | python3 file_reader_secure.py

Run the final verification scan:

bandit *_secure.py -ll

Verify final structure:

tree

## Vulnerabilities Demonstrated

- SQL injection through unsafe string-formatted SQL queries
- Path traversal through unsafe file path construction
- Command injection through unsanitized shell command execution
- Weak password hashing demonstration
- Missing input validation
- Unsafe user-controlled command arguments

## Security Controls Implemented

- Parameterized SQL queries
- Username validation
- Password hashing demonstration
- Path normalization with pathlib
- Base-directory containment checks
- Safe subprocess execution with argument lists
- Hostname validation
- Timeout enforcement for subprocess calls
- Static application security testing with Bandit

## Tools Used

- Python 3
- SQLite
- pathlib
- subprocess
- hashlib
- re
- Bandit
- Safety
- Pylint
- Bash
- Linux
- Git
- tree

## Key Skills Demonstrated

- Secure code review
- Application security hardening
- Static application security testing
- SQL injection prevention
- Path traversal mitigation
- Command injection prevention
- Input validation
- Secure subprocess usage
- Python security remediation
- DevSecOps validation workflow
- AI-generated code risk assessment
- Secure software development fundamentals

## Real-World Use Case

Engineering teams increasingly use AI tools to generate application code, automation scripts, and backend utilities. This workflow demonstrates how AppSec, DevSecOps, and Security Engineering teams can review AI-produced code, detect insecure patterns with static analysis, refactor vulnerable implementations, and verify that dangerous coding patterns are removed before deployment.

## Lessons Learned

- AI-generated code can be functional while still containing serious security vulnerabilities.
- Static analysis helps identify common insecure patterns early in development.
- Parameterized queries are required to prevent SQL injection.
- File access must validate resolved paths against an approved base directory.
- Shell command execution should avoid string-based commands and use argument lists instead.
- SHA-256 is not suitable for production password storage; bcrypt or Argon2 should be used in real systems.

## Troubleshooting Log

Issue:
Global Python package installation can fail on Ubuntu 24.04 because of externally managed Python behavior.

Resolution:
Created and used a Python virtual environment before installing Bandit, Safety, and Pylint.

Issue:
Bandit reliably flags SQL injection and command execution risks, but path traversal detection may require manual review or additional tools.

Resolution:
Documented the limitation and hardened the file reader manually using pathlib path resolution and base-directory containment checks.

Issue:
The secure command executor still executes ping, which Bandit may warn about depending on severity settings.

Resolution:
Used subprocess.run with an argument list, input validation, timeout control, and shell-free execution.

Issue:
The password hashing example uses SHA-256.

Resolution:
Kept SHA-256 only for demonstration and documented that production systems should use bcrypt or Argon2.

Issue:
The secure file reader returns file not found for some traversal attempts because os.path.basename strips directory traversal components.

Resolution:
Accepted this as safe behavior because the dangerous path is not accessed and the final resolved path stays inside the allowed upload directory.
