# Secure Configuration Validator

## What This Does

This implementation provides a Python-based configuration security validator for YAML application configuration files. It loads configuration files safely, validates required sections and fields, checks file permissions, and detects common security risks such as weak passwords, insecure HTTP endpoints, disabled SSL/TLS, privileged usernames, debug logging, and unsafe feature flags.

The validator is designed to catch dangerous configuration issues before an application is deployed or promoted into production. It supports multiple configuration files in a single run and generates structured validation reports that separate critical errors from security warnings.

This type of automation helps DevSecOps, Security Engineering, Platform Engineering, Cloud Security, and Application Security teams enforce secure configuration standards consistently across environments.

## Architecture

    +-----------------------------+
    | YAML Configuration Files     |
    | config_secure.yaml           |
    | config_insecure.yaml         |
    | config_incomplete.yaml       |
    | config_test.yaml             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Secure Loader Layer          |
    | config_validator.py          |
    | - File existence checks      |
    | - File type checks           |
    | - Permission inspection      |
    | - Safe YAML parsing          |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Validation Engine            |
    | - Required schema checks     |
    | - Weak password detection    |
    | - HTTP endpoint detection    |
    | - SSL/TLS disabled checks    |
    | - Privileged user checks     |
    | - Debug mode checks          |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Report Output       |
    | - Critical errors            |
    | - Security warnings          |
    | - Per-file validation result |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python virtual environments
- Python pip
- PyYAML
- Git
- tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/config-security-validator

cd ~/config-security-validator

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

pip install pyyaml

## How to Reproduce

Activate the Python virtual environment:

source venv/bin/activate

Run the validator against all bundled configuration files:

python3 config_validator.py

Run the validator against one specific configuration file:

python3 config_validator.py config_insecure.yaml

Test permission warning detection:

chmod 644 config_secure.yaml

python3 config_validator.py config_secure.yaml

Restore secure permissions:

chmod 600 config_secure.yaml

Verify Python syntax:

python3 -m py_compile config_validator.py

Review files and permissions:

tree .

ls -l config_*.yaml config_validator.py

## Configuration Files Included

- config_secure.yaml: secure baseline configuration with strong password, HTTPS endpoint, SSL enabled, and INFO logging.
- config_insecure.yaml: intentionally insecure configuration with weak password, root database user, HTTP endpoint, disabled SSL, DEBUG logging, and world-readable permissions.
- config_incomplete.yaml: intentionally incomplete configuration missing required fields for validation testing.
- config_test.yaml: additional negative test case containing weak password, privileged user, HTTP endpoint, disabled SSL, debug logging, unsafe mode, and enabled admin panel.

## Tools Used

- Python 3
- PyYAML
- Bash
- YAML
- Linux file permissions
- chmod
- stat
- pathlib
- argparse
- Git
- tree

## Key Skills Demonstrated

- Secure configuration validation
- YAML parsing with safe_load
- Python security automation
- DevSecOps control implementation
- Required schema enforcement
- File permission auditing
- Weak password detection
- Insecure protocol detection
- SSL/TLS configuration validation
- Dangerous runtime setting detection
- CLI utility design
- Defensive input handling
- Structured security report generation
- Application security testing

## Real-World Use Case

Engineering teams can use this validator as a pre-deployment security gate for application configuration files. For example, before promoting a service to staging or production, a CI/CD workflow could run this tool to detect weak passwords, unsafe debug settings, disabled TLS, HTTP endpoints, missing required fields, or overly permissive configuration file permissions. This reduces the risk of configuration-driven incidents and helps enforce secure defaults across cloud, container, and platform environments.

## Lessons Learned

- Global pip installation can fail or create dependency hygiene problems on Ubuntu 24.04 because Python is externally managed, so dependencies should be installed inside a virtual environment.
- YAML files should be parsed with yaml.safe_load instead of unsafe loading methods.
- File permissions are part of configuration security because world-readable files may expose secrets.
- Required schemas should include security-critical fields such as SSL/TLS enablement.
- Validation tools are more useful when they accept one or many config files through command-line arguments.
- Negative test files are important because they prove the validator actually detects insecure conditions.

## Troubleshooting Log

Issue:
Ubuntu 24.04 can reject global pip package installation due to externally managed Python environments.

Resolution:
Created a Python virtual environment with python3 -m venv and installed PyYAML inside the isolated environment.

Issue:
The starter script imported unused modules including json, re, Tuple, and jsonschema.

Resolution:
Removed unused imports and kept only the modules required by the implemented validator.

Issue:
The original required schema did not require database.ssl_enabled even though TLS validation was a core security objective.

Resolution:
Added database.ssl_enabled as a required field so incomplete security configurations are flagged.

Issue:
The original weak password check only flagged passwords shorter than 8 characters.

Resolution:
Strengthened password validation by flagging passwords shorter than 12 characters and checking for uppercase, lowercase, digit, and special-character requirements.

Issue:
The original validator only accepted a fixed list of configuration files.

Resolution:
Implemented argparse support so the validator can scan default files or any specific YAML file passed on the command line.

Issue:
World-readable file warnings needed a repeatable test.

Resolution:
Kept intentionally insecure test files with 644 permissions and verified that permission warnings appear in the generated report.
