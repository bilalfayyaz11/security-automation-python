# Secure Token and Secret Generator

## What This Does

This implementation provides a secure Python-based utility for generating application tokens, API keys, passwords, OTP secrets, CSRF tokens, password reset tokens, and credential files.

The system uses Python's cryptographically secure secrets module instead of the insecure random module, ensuring generated values are suitable for authentication, authorization, session management, API access, and security-sensitive workflows.

Generated credentials are stored in JSON files with restrictive 600 permissions, helping prevent accidental exposure through weak filesystem access controls.

## Architecture

    +-----------------------------+
    | Python Security Toolkit     |
    | secrets / string / json     |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Randomness Demonstration    |
    | random_comparison.py        |
    | random vs secrets           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Token Generation Layer      |
    | token_generator.py          |
    | Hex / URL-safe / Alpha      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Credential Generation Layer |
    | api_key_generator.py        |
    | API Keys / Passwords        |
    | Webhook Secrets             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Interactive Token Manager   |
    | token_manager.py            |
    | Session / CSRF / Reset      |
    | OTP / API Credential Sets   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Secure Local Storage        |
    | credentials.json            |
    | tokens.json                 |
    | chmod 600 permissions       |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Verification Layer          |
    | verify_tokens.py            |
    | Entropy + Uniqueness Checks |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3.12 or higher
- Python pip
- Bash
- Git
- tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip tree git

mkdir -p ~/secure-token-lab

cd ~/secure-token-lab

python3 --version

pip3 --version

## How to Reproduce

Run the randomness comparison:

python3 random_comparison.py

Run it again to observe that the seeded random module produces predictable values while the secrets module produces new secure values:

python3 random_comparison.py

Generate secure tokens:

python3 token_generator.py

Verify each run creates different tokens:

for i in {1..3}; do echo "Run $i:"; python3 token_generator.py | head -n 5; echo ""; done

Generate API keys, secrets, and passwords:

python3 api_key_generator.py

Verify the generated credentials file uses owner-only permissions:

ls -l credentials.json

View the generated credential structure:

cat credentials.json

Run the interactive token manager:

python3 token_manager.py

Run an automated token manager test:

printf "1\n2\n3\n4\n5\n6\nmyapp\n7\n" | python3 token_manager.py

Verify saved tokens:

ls -l tokens.json

cat tokens.json

Run uniqueness verification:

python3 verify_tokens.py

Check token entropy:

python3 -c "import secrets; print(f'Token entropy: {len(secrets.token_hex(32)) * 4} bits')"

Run final script checks:

python3 token_generator.py > /dev/null && echo "token_generator.py: OK"

python3 api_key_generator.py > /dev/null && echo "api_key_generator.py: OK"

printf "6\nmyapp\n7\n" | python3 token_manager.py > /dev/null && echo "token_manager.py: OK"

python3 verify_tokens.py > /dev/null && echo "verify_tokens.py: OK"

## Tools Used

- Python 3
- Python secrets module
- Python string module
- Python json module
- Python base64 module
- Python os module
- Bash
- Linux file permissions
- Git
- tree

## Key Skills Demonstrated

- Cryptographically secure token generation
- Secure API key design
- Password generation
- CSRF token generation
- Session token generation
- Password reset token generation
- OTP secret generation
- Secure credential file storage
- Linux permission hardening with chmod 600
- Entropy verification
- Token uniqueness testing
- Python security scripting
- Developer security tooling
- DevSecOps utility development

## Real-World Use Case

Engineering and security teams frequently need secure credentials for internal services, API authentication, webhook signing, application sessions, password reset flows, two-factor authentication setup, and deployment automation. This utility demonstrates how to generate those values safely using cryptographic randomness while protecting stored credential files with restrictive filesystem permissions.

## Lessons Learned

- Python's random module is predictable when seeded and should not be used for security-sensitive values.
- Python's secrets module is designed for cryptographic randomness and is appropriate for tokens, keys, and passwords.
- API keys benefit from readable prefixes because they help identify key type and usage.
- Credential files should use restrictive permissions such as 600 to reduce accidental exposure.
- Token length should be understood in terms of entropy, not only visible character count.
- Secrets should never be committed to public repositories in real production environments.

## Troubleshooting Log

Issue:
pip3 was missing from the fresh Ubuntu 24.04 environment.

Resolution:
Installed python3-pip through apt even though the lab scripts only use Python built-in modules.

Issue:
The lab files were created directly under /home/ubuntu instead of /home/ubuntu/secure-token-lab.

Resolution:
Moved all generated Python scripts and JSON artifacts into ~/secure-token-lab before preparing the repository structure.

Issue:
The original password generator could produce passwords without uppercase, lowercase, digit, or special-character coverage.

Resolution:
Improved the password generator to keep generating until the password includes required character categories.

Issue:
The original token manager saved sensitive token output in plaintext JSON.

Resolution:
Kept the lab behavior for demonstration but enforced chmod 600 permissions and documented that production systems should use secret managers or encryption.

Issue:
Running the interactive menu manually is slower and less reproducible.

Resolution:
Used printf input automation to test menu options consistently from the terminal.
