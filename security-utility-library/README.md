
# Security Utility Library

## What This Does

This implementation provides a reusable Python security utility library containing password validation and cryptographic hashing capabilities. The library is organized into modular packages that can be imported into security automation, DevSecOps, compliance, and application security workflows.

The password validation module enforces common password security requirements such as minimum length, uppercase characters, lowercase characters, numeric digits, and special characters. The hashing module provides SHA-256 hashing, file integrity verification, and hash comparison functionality.

The project demonstrates secure coding practices, package design, testing methodologies, and reusable security component development suitable for production automation environments.

## Architecture

```
+----------------------------------+
| Applications & Automation Tools  |
+----------------+-----------------+
                 |
                 v
+----------------------------------+
| Security Utility Library         |
| securitylib                      |
+----------------+-----------------+
                 |
     +-----------+-----------+
     |                       |
     v                       v
+-----------+         +-------------+
| Password  |         | Hashing     |
| Validator |         | Utilities   |
| Module    |         | Module      |
+-----+-----+         +------+------+
      |                      |
      v                      v
+-----------+         +-------------+
| Strength  |         | SHA-256     |
| Checks    |         | File Hashes |
| Policy    |         | Verification|
+-----------+         +-------------+
             \       /
              \     /
               v   v
         +-------------+
         | Test Suite  |
         | CLI Demo    |
         +-------------+
```

## Prerequisites

* Ubuntu 24.04
* Python 3.12+
* python3-pip
* Git
* tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip tree git

mkdir -p ~/security-utility-library

cd ~/security-utility-library

## How to Reproduce

Run the complete test suite:

python3 tests/test_security.py

Test password validation:

python3 -c "from securitylib.password import validator; print(validator.validate_password('Test123!'))"

Test SHA-256 hashing:

python3 -c "from securitylib.hash import hasher; print(hasher.hash_sha256('test'))"

Run interactive demonstration:

python3 demo_tool.py

View project structure:

tree -a -L 3

## Tools Used

* Python 3
* hashlib
* Linux
* Bash
* Git
* SHA-256
* Package Architecture
* Security Validation

## Key Skills Demonstrated

* Secure software development
* Modular Python package design
* Password policy enforcement
* Cryptographic hashing
* File integrity verification
* Security utility development
* Test-driven validation
* Python import systems
* Reusable library architecture
* Security automation foundations

## Real-World Use Case

Organizations frequently require reusable security functions across multiple applications and automation workflows. Password validation is commonly used in identity management systems, account provisioning tools, internal applications, and compliance controls. Hashing functions are widely used for file integrity monitoring, security auditing, artifact verification, and secure data processing. This library provides a reusable foundation that can be integrated into larger security platforms and automation systems.

## Lessons Learned

* Modular architecture improves maintainability and reuse.
* Security controls should be implemented as reusable libraries rather than duplicated code.
* Package initialization simplifies imports and improves usability.
* Hash verification provides a simple mechanism for integrity validation.
* Comprehensive testing is essential for security-related functionality.

## Troubleshooting Log

Issue:
Fresh Ubuntu environment did not include pip3.

Resolution:
Installed python3-pip through apt.

Issue:
Fresh Ubuntu environment did not include tree.

Resolution:
Installed tree through apt.

Issue:
Python package imports can fail when package initialization files are missing.

Resolution:
Created **init**.py files in all package directories.

Issue:
Python cache directories appeared after execution.

Resolution:
Removed **pycache** directories before repository upload and added .gitignore rules.

Issue:
Starter implementation contained unfinished TODO sections.

Resolution:
Implemented complete password validation, hashing, verification, and testing functionality.
