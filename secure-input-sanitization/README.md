# Secure Input Sanitization Framework

## What This Does

This implementation provides a reusable Python-based input validation and sanitization framework designed to identify, reject, or neutralize unsafe user input before it reaches application logic, operating system commands, filesystems, databases, or web interfaces.

The framework demonstrates multiple defensive controls including command injection prevention, path traversal protection, SQL injection detection, HTML escaping, email validation, username validation, and secure filename handling.

The solution includes both vulnerable and secure implementations to demonstrate the security risks associated with unsafe input handling and the practical techniques used to mitigate them.

These controls are commonly implemented within web applications, APIs, internal tooling, automation platforms, identity systems, and security-focused applications.

## Architecture

    +-----------------------------+
    | User Input                  |
    | Username                    |
    | Email                       |
    | Comments                    |
    | Filenames                   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Input Sanitizer Engine      |
    | Regex Validation            |
    | Character Filtering         |
    | HTML Escaping               |
    | SQL Detection               |
    | Path Validation             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Controls           |
    | XSS Protection              |
    | SQL Injection Detection     |
    | Command Injection Defense   |
    | Path Traversal Prevention   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Secure Application Layer    |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Git
- Linux shell

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip git tree

git clone <repository-url>

cd secure-input-sanitization

chmod +x *.py

## How to Reproduce

Run the vulnerable demonstration:

python3 vulnerable_app.py

Run the secure implementation:

python3 secure_app.py

Run verification tests:

python3 verify_lab.py

Run interactive testing:

python3 interactive_test.py

## Tools Used

- Python 3
- Regex
- HTML Escaping
- Linux
- Git

## Key Skills Demonstrated

- Secure coding practices
- Input validation
- Input sanitization
- Regular expression validation
- SQL injection detection
- Cross-site scripting prevention
- Path traversal protection
- Command injection awareness
- Defensive programming
- Application security fundamentals

## Real-World Use Case

Organizations processing user-generated content must treat all input as untrusted. Input validation and sanitization are critical controls within web applications, APIs, customer portals, administrative interfaces, authentication systems, and internal automation platforms. These controls reduce the risk of exploitation through malformed, malicious, or unexpected user input and form a foundational component of secure software development.

## Lessons Learned

- User input should never be trusted.
- Validation and sanitization serve different purposes and should be combined.
- HTML escaping is essential when rendering user content.
- Filename validation helps prevent path traversal attacks.
- Security controls should be centralized into reusable libraries.

## Troubleshooting Log

Issue:
Unsafe shell command execution allowed command injection.

Resolution:
Implemented validation and sanitization before processing user input.

Issue:
Filename handling allowed path traversal attempts.

Resolution:
Restricted filenames using basename extraction and character filtering.

Issue:
User content could contain HTML and JavaScript.

Resolution:
Implemented HTML escaping using Python's html module.

Issue:
SQL keywords could be embedded within input.

Resolution:
Implemented SQL injection pattern detection.

Issue:
Validation logic duplicated across components.

Resolution:
Centralized controls into the InputSanitizer class.
