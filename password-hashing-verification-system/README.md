# Password Hashing and Verification System

## What This Does

This implementation provides a secure password hashing and verification system using bcrypt. It demonstrates the danger of plain-text password storage, then implements secure user registration, bcrypt-based password hashing, automatic salt generation, password verification, secure JSON-based credential storage, and an interactive command-line authentication interface.

The secure manager stores only bcrypt hashes and password metadata, never plain-text passwords. It also restricts the secure credential file to owner-only permissions so stored password hashes are not exposed unnecessarily to other local users.

This type of system is foundational for application security, identity systems, authentication services, DevSecOps workflows, and secure software engineering.

## Architecture

    +-----------------------------+
    | User Input                   |
    | username / password          |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Password Manager             |
    | secure_password_manager.py   |
    | - Registration               |
    | - Hashing                    |
    | - Verification               |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | bcrypt Security Layer        |
    | - Unique salt per password   |
    | - Configurable cost rounds   |
    | - One-way hash output        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Secure Credential Store      |
    | secure_passwords.json        |
    | chmod 600 permissions        |
    | hash + algorithm metadata    |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python virtual environments
- Python pip
- bcrypt
- tree
- Git

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv tree git

mkdir -p ~/password-hashing-verification-system

cd ~/password-hashing-verification-system

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

pip install bcrypt

## How to Reproduce

Run the insecure plain-text demonstration:

venv/bin/python plain_text_demo.py

View insecure storage:

cat insecure_passwords.txt

Run the secure password manager:

venv/bin/python secure_password_manager.py

View secure hashed storage:

cat secure_passwords.json

Check secure storage permissions:

ls -l secure_passwords.json

Verify bcrypt salt behavior:

venv/bin/python test_salt.py

Run automated password manager tests:

venv/bin/python test_password_manager.py

Compare insecure and secure storage:

cat insecure_passwords.txt

cat secure_passwords.json

Run the interactive CLI:

venv/bin/python password_cli.py

Verify Python syntax:

venv/bin/python -m py_compile plain_text_demo.py secure_password_manager.py password_cli.py test_salt.py test_password_manager.py

Review file tree:

tree .

## Tools Used

- Python 3
- bcrypt
- JSON
- getpass
- pathlib
- os.chmod
- Bash
- Linux file permissions
- tree
- Git

## Key Skills Demonstrated

- Secure password hashing
- bcrypt implementation
- Automatic salt generation
- Password verification with bcrypt.checkpw
- Plain-text password risk demonstration
- Secure credential storage
- File permission hardening
- Authentication CLI design
- Automated security testing
- Secure coding practices
- IAM and application security fundamentals
- Credential protection workflow design

## Real-World Use Case

A web application, internal platform, or authentication service can use bcrypt-based password hashing to protect user credentials. If a database is breached, attackers should not be able to read plain-text passwords. Instead, they only receive salted bcrypt hashes, which are intentionally expensive to crack. This implementation demonstrates the same core workflow used in production authentication systems: hash passwords during registration, store only the hash, and verify future login attempts using bcrypt comparison.

## Lessons Learned

- Plain-text password storage is dangerous because anyone with file or database access can immediately read user credentials.
- bcrypt automatically embeds a unique salt into each password hash, so the same password produces different hashes each time.
- Password hashes should be treated as sensitive data and stored with restricted file permissions.
- Password verification should compare the submitted password against the stored hash, not decrypt anything.
- Using a proven library like bcrypt is safer than designing custom password hashing logic.

## Troubleshooting Log

Issue:
Global pip installation can fail or create dependency hygiene problems on Ubuntu 24.04.

Resolution:
Created a Python virtual environment and installed bcrypt inside the isolated environment.

Issue:
The starter secure storage format mapped usernames directly to hash strings only.

Resolution:
Expanded the storage format to include password_hash, algorithm, and bcrypt_rounds metadata.

Issue:
The original secure password file was saved without explicit permission hardening.

Resolution:
Added os.chmod with mode 600 after saving secure_passwords.json.

Issue:
The insecure demonstration originally used a basic split operation that could break if password values contained a colon.

Resolution:
Used split(":", 1) to avoid breaking the parser on extra colon characters.

Issue:
The lab relied mostly on manual testing.

Resolution:
Added test_password_manager.py to validate registration, duplicate-user rejection, correct-password verification, wrong-password rejection, missing-user handling, and absence of plain-text passwords in secure storage.
