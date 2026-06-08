# HTTP Header Security Analyzer

## What This Does

This implementation provides a Python-based HTTP response header security analyzer for web application security assessment. It fetches HTTP headers from a target URL, identifies missing browser security controls, detects insecure header configurations, calculates a security score, and optionally writes a JSON report for automation workflows.

The analyzer checks important security headers including Strict-Transport-Security, Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, Cross-Origin-Opener-Policy, and Cross-Origin-Resource-Policy. It also detects weak configurations such as disabled XSS protection, unsafe CSP directives, missing HSTS max-age, low HSTS max-age, and insecure frame options.

This type of tool is useful for DevSecOps, Application Security, Cloud Security, SOC automation, and web hardening workflows where teams need fast visibility into HTTP security posture.

## Architecture

    +-----------------------------+
    | Target Web Server            |
    | example.com / github.com     |
    | localhost test server        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Header Fetching Layer        |
    | requests.get                 |
    | - Timeout handling           |
    | - Redirect handling          |
    | - TLS validation             |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Analysis Engine     |
    | header_analyzer.py           |
    | - Missing header checks      |
    | - Insecure value checks      |
    | - HSTS validation            |
    | - CSP validation             |
    | - Security scoring           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Reporting Layer              |
    | Console report               |
    | JSON report                  |
    | Color-coded findings         |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python virtual environments
- Python pip
- Requests
- Colorama
- curl
- tree
- Git

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv curl tree git

mkdir -p ~/http-header-analyzer

cd ~/http-header-analyzer

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

pip install requests colorama

## How to Reproduce

Activate the Python virtual environment:

source venv/bin/activate

Analyze a public website:

venv/bin/python header_analyzer.py https://example.com --json-output example_report.json

Analyze a domain without manually adding HTTPS:

venv/bin/python header_analyzer.py github.com --json-output github_report.json

Start the local test server:

nohup venv/bin/python test_server.py > test_server.log 2>&1 &

echo $! > test_server.pid

sleep 2

Analyze the local test server:

venv/bin/python header_analyzer.py http://localhost:8000 --json-output local_test_report.json

Review the JSON report:

python3 -m json.tool local_test_report.json

Stop the local test server:

kill "$(cat test_server.pid)"

Verify Python syntax:

venv/bin/python -m py_compile header_analyzer.py test_server.py

Review the file tree:

tree .

## Tools Used

- Python 3
- Requests
- Colorama
- argparse
- JSON
- regular expressions
- http.server
- Bash
- Linux
- curl
- tree
- Git

## Key Skills Demonstrated

- HTTP header inspection
- Web security assessment automation
- Application security testing
- Security header validation
- HSTS configuration analysis
- CSP configuration analysis
- TLS-aware HTTP requests
- CLI utility design
- JSON report generation
- Local test server simulation
- DevSecOps security control validation
- Browser security hardening analysis

## Real-World Use Case

Security teams can use this analyzer during web application reviews, pre-production checks, or continuous security validation to identify missing or weak HTTP security headers. For example, before a service is promoted to production, a DevSecOps pipeline could run this tool against the deployed endpoint and fail the release if high-risk headers like Strict-Transport-Security or Content-Security-Policy are missing. The JSON output can also feed dashboards, ticketing workflows, or automated security reporting systems.

## Lessons Learned

- HTTP security headers are a lightweight but important browser-side defense layer.
- Missing HSTS, CSP, and frame protection headers can expose applications to avoidable risks.
- Header names should be compared case-insensitively because HTTP headers are not case-sensitive.
- TLS verification should remain enabled by default; bypassing certificate validation should only be an explicit testing option.
- JSON output makes security tools easier to integrate with CI/CD, dashboards, and automated reporting.

## Troubleshooting Log

Issue:
The starter fetch_headers function only contained pass and did not actually retrieve headers.

Resolution:
Implemented requests.get with timeout, redirect support, TLS verification, a custom User-Agent, and structured error handling.

Issue:
Global pip installation can fail or create dependency hygiene problems on Ubuntu 24.04.

Resolution:
Created a Python virtual environment and installed Requests and Colorama inside the isolated environment.

Issue:
The original troubleshooting guidance suggested verify=False for SSL certificate errors.

Resolution:
Kept TLS verification enabled by default and exposed certificate bypass only through an explicit --insecure-skip-tls-verify testing flag.

Issue:
Basic missing-header checks alone do not detect weak values.

Resolution:
Added insecure configuration checks for weak X-Frame-Options, disabled X-XSS-Protection, missing or low HSTS max-age, missing includeSubDomains, and risky CSP directives.

Issue:
Manual console output is not enough for automation.

Resolution:
Added optional JSON report generation using --json-output so results can be consumed by scripts, pipelines, dashboards, or security automation.
