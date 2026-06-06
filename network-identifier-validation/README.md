# Network Identifier Validation Toolkit

## What This Does

This implementation provides a Python-based validation toolkit for network identifiers including IPv4 addresses, IPv6 addresses, and RFC-compliant hostnames.

The solution performs format validation, detects malformed identifiers, and automatically classifies network identifiers into the correct category before validation. The toolkit combines manual validation logic and Python networking libraries to provide reliable validation for infrastructure and security workflows.

This type of validation is commonly used in firewall automation, DNS management systems, cloud infrastructure tooling, SIEM platforms, network scanners, asset inventory systems, and security monitoring solutions.

## Architecture

    +----------------------------------+
    | User Input                       |
    | IPv4 / IPv6 / Hostname           |
    +----------------+-----------------+
                     |
                     v
    +----------------------------------+
    | Detection Engine                 |
    | Type Classification              |
    +----------------+-----------------+
                     |
        +------------+------------+
        |                         |
        v                         v
+---------------+       +------------------+
| IPv4 Validator|       | IPv6 Validator   |
| Manual Parsing|       | ipaddress Module |
+-------+-------+       +---------+--------+
        |                         |
        +------------+------------+
                     |
                     v
          +----------------------+
          | Hostname Validator   |
          | RFC Rules + Regex    |
          +----------+-----------+
                     |
                     v
          +----------------------+
          | Validation Result    |
          +----------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3.12+
- Git
- tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 git tree

chmod +x *.py

## How to Reproduce

Run IPv4 validation:

python3 ipv4_validator.py

Run IPv6 validation:

python3 ipv6_validator.py

Run hostname validation:

python3 hostname_validator.py

Run combined validation:

python3 network_validator.py

Example inputs:

192.168.1.1

2001:db8::1

example.com

256.1.1.1

-invalid.com

quit

## Tools Used

- Python 3
- ipaddress
- Regular Expressions
- Linux
- Git

## Key Skills Demonstrated

- IPv4 validation
- IPv6 validation
- Hostname validation
- RFC-compliant hostname validation
- Regular expression development
- Network automation fundamentals
- Security-focused validation logic
- Input validation
- Defensive programming

## Real-World Use Case

Network identifiers are continuously entered into firewalls, cloud security groups, DNS records, inventory systems, vulnerability scanners, monitoring platforms, and security automation tools. Incorrectly formatted identifiers can cause configuration failures, service outages, and security issues. This toolkit provides a reusable validation layer that can be integrated into infrastructure automation pipelines and security tooling.

## Lessons Learned

- IPv4 validation can be implemented through manual parsing and range checking.
- IPv6 validation is more reliable using Python's built-in ipaddress module.
- Hostname validation requires RFC-compliant label validation.
- IPv4-like values require special handling to avoid hostname misclassification.
- Validation logic should be separated into reusable components.

## Troubleshooting Log

Issue:
The original combined validator incorrectly classified 256.1.1.1 as a valid hostname.

Resolution:
Added explicit IPv4-pattern detection before hostname validation.

Issue:
The lab instructed installation of ipaddress via pip.

Resolution:
Python 3.12 already includes the ipaddress module.

Issue:
Hostname validation required label-length enforcement.

Resolution:
Added validation for labels between 1 and 63 characters.

Issue:
Network identifier classification order was important.

Resolution:
Implemented IPv4 → IPv6 → Hostname detection priority.
