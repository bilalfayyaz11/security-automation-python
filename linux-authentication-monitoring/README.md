# Linux Authentication Monitoring Toolkit

## What This Does

This implementation provides a Linux authentication log monitoring toolkit that analyzes SSH login activity, failed authentication attempts, successful logins, invalid user attempts, root login attempts, and brute-force indicators.

The toolkit uses Bash, awk, grep, and Linux authentication logs to generate structured security reports from `/var/log/auth.log`. It includes separate analyzers for failed logins, successful logins, security alerts, and a complete dashboard report.

This type of automation is useful for SOC teams, Linux administrators, platform engineers, cloud engineers, and security analysts who need fast visibility into authentication behavior on Linux servers.

## Architecture

    +--------------------------------+
    | Linux Authentication Logs      |
    | /var/log/auth.log              |
    +---------------+----------------+
                    |
                    v
    +--------------------------------+
    | Log Filtering Layer            |
    | sshd event filtering           |
    | sudo command exclusion         |
    | false-positive removal         |
    +---------------+----------------+
                    |
                    v
    +--------------------------------+
    | Analysis Scripts               |
    | failed_logins.sh               |
    | successful_logins.sh           |
    | security_alerts.sh             |
    | auth_analyzer.sh               |
    +---------------+----------------+
                    |
                    v
    +--------------------------------+
    | Security Reports               |
    | Failed login summary           |
    | Successful login summary       |
    | Brute-force indicators         |
    | Root login warnings            |
    | Invalid user detection         |
    +--------------------------------+

## Prerequisites

- Ubuntu 24.04
- Bash
- grep
- awk
- sed
- Git
- tree
- sudo access
- Access to `/var/log/auth.log`

## Setup & Installation

sudo apt update

sudo apt install -y git grep gawk sed tree

mkdir -p ~/linux-authentication-monitoring

cd ~/linux-authentication-monitoring

## How to Reproduce

Run the failed login analyzer:

./failed_logins.sh

Run the successful login analyzer:

./successful_logins.sh

Run the security alert analyzer:

./security_alerts.sh

Run the complete authentication dashboard:

./auth_analyzer.sh

Analyze a custom authentication log file:

./auth_analyzer.sh /var/log/auth.log.1

Validate all scripts:

bash -n *.sh

Inspect repository structure:

tree

## Tools Used

- Bash
- grep
- awk
- sed
- Linux authentication logs
- OpenSSH log events
- sudo audit logs
- tree
- Git

## Key Skills Demonstrated

- Linux authentication log analysis
- SSH security monitoring
- Failed login detection
- Successful login tracking
- Brute-force pattern identification
- Invalid user detection
- Root login attempt monitoring
- Bash automation
- awk-based log parsing
- False-positive reduction
- SOC-style security reporting
- Blue Team operational visibility

## Real-World Use Case

Production Linux servers are constant targets for SSH brute-force attempts, invalid username enumeration, root login attempts, and unauthorized access attempts. This toolkit provides a lightweight security monitoring layer that helps engineers quickly identify suspicious authentication behavior without manually reading raw log files. In a real company, this could be extended into cron-based monitoring, SIEM forwarding, Slack alerts, or automated incident response workflows.

## Lessons Learned

- Authentication log formats vary across Linux versions and cloud images.
- Fixed awk field numbers can break when timestamp formats change.
- Searching logs with sudo can create new sudo audit entries that pollute future searches.
- Reliable log analysis requires filtering real sshd events and excluding command audit noise.
- Small Bash scripts can provide meaningful first-level security visibility before full SIEM integration.

## Troubleshooting Log

Issue:
Ubuntu 24.04 authentication logs used ISO-style timestamps instead of older syslog-style timestamps.

Resolution:
Avoided fixed timestamp field assumptions and extracted values using keywords such as Accepted, Failed password, for, and from.

Issue:
Initial grep commands created false positives because sudo logged the search command itself into auth.log.

Resolution:
Excluded sudo command audit entries containing COMMAND= from all analysis scripts.

Issue:
Failed password searches returned lines created by the search commands instead of real SSH failures.

Resolution:
Filtered only real sshd authentication events and excluded command audit noise.

Issue:
The environment had no real failed SSH password attempts.

Resolution:
Scripts were designed to safely report zero findings without failing or producing misleading output.

Issue:
The original fixed awk field extraction was fragile across Linux distributions.

Resolution:
Implemented keyword-based parsing for usernames, source IP addresses, authentication methods, and security indicators.
