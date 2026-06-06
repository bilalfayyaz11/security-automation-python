
# Requirement-Driven Python Function Generator

## What This Does

This implementation provides a lightweight requirement analysis and code generation utility that converts natural-language requirements into executable Python function templates.

The system parses human-readable specifications, identifies action verbs and targets, generates structured metadata, and automatically creates Python function skeletons that developers can extend with production logic.

This approach reduces repetitive development work and provides a foundation for requirement-to-code automation workflows commonly used in security automation, platform engineering, compliance tooling, and internal developer platforms.

## Architecture

```
+--------------------------------------+
| Natural Language Requirements        |
| "validate password strength"         |
| "scan network ports"                 |
| "verify email format"                |
+------------------+-------------------+
                   |
                   v
+--------------------------------------+
| Requirement Parser                   |
| requirement_parser.py                |
| Action Extraction                    |
| Target Identification                |
| Function Name Generation             |
+------------------+-------------------+
                   |
                   v
+--------------------------------------+
| Template Generation Engine           |
| Python Function Builder              |
| Docstring Generator                  |
| Skeleton Code Creation               |
+------------------+-------------------+
                   |
                   v
+--------------------------------------+
| Generated Python Functions           |
| validate_user_password_strength.py   |
| check_file_permissions.py            |
| scan_network_ports.py                |
| encrypt_sensitive_data.py            |
+------------------+-------------------+
                   |
                   v
+--------------------------------------+
| Custom Implementations               |
| Password Validation Logic            |
| Future Security Controls             |
+--------------------------------------+
```

## Prerequisites

* Ubuntu 24.04
* Python 3.12+
* Python pip
* Python virtual environments
* Git
* tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/requirement-driven-code-generation

cd ~/requirement-driven-code-generation

## How to Reproduce

Create the parser:

python3 requirement_parser.py

Verify generated files:

ls -la *.py

Implement password validation:

python3 validate_user_password_strength.py

Generate a custom requirement:

python3 test_custom_requirement.py

Validate all Python files:

python3 -m py_compile *.py

Inspect project structure:

tree

## Tools Used

* Python 3
* Regular Expressions (re)
* Linux
* Bash
* Git
* tree

## Key Skills Demonstrated

* Natural-language requirement analysis
* Requirement parsing
* Code generation automation
* Python string processing
* Regex-based pattern matching
* Template generation
* Security automation foundations
* Developer productivity tooling
* Automation workflow design
* Functional decomposition

## Real-World Use Case

Engineering, security, compliance, and platform teams regularly receive requirements written in natural language by stakeholders. This utility demonstrates how those requirements can be systematically transformed into executable code templates. Similar techniques are used in internal developer platforms, policy-as-code systems, security automation frameworks, and AI-assisted software engineering workflows to accelerate implementation while maintaining consistency.

## Lessons Learned

* Requirement parsing becomes more reliable when action verbs are extracted using regex boundaries.
* Consistent naming conventions simplify automated code generation.
* Template generation can eliminate repetitive developer tasks.
* Structured metadata provides a bridge between human requirements and machine execution.
* Small automation utilities often become foundational building blocks for larger engineering platforms.

## Troubleshooting Log

Issue:
Ubuntu 24.04 environment did not include pip3 by default.

Resolution:
Installed python3-pip using apt.

Issue:
tree utility was not available in the fresh environment.

Resolution:
Installed tree using apt.

Issue:
Action detection could incorrectly match partial words when using basic substring searches.

Resolution:
Replaced substring matching with regex word-boundary matching.

Issue:
Generated function names could contain invalid characters.

Resolution:
Implemented regex sanitization to generate valid Python identifiers.

Issue:
Generated templates initially provided placeholder logic only.

Resolution:
Implemented a production-style password validation example demonstrating real functionality.
