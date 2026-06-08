# DNS Anomaly Monitoring Toolkit

## What This Does

This implementation provides a DNS resolution and anomaly monitoring toolkit for security analysis. It performs DNS lookups, logs domain query results, simulates suspicious DNS behaviors, and detects abnormal domain patterns such as high-entropy DGA-style names, unusually long domains, numeric-heavy labels, and IP-encoded domains.

The toolkit includes a Bash DNS query logger, a Python DNS resolver, a DNS anomaly simulator, and a DNS anomaly detector with risk classification and JSON reporting. It is designed to demonstrate how DNS behavior can be analyzed for early signs of malware infrastructure, phishing activity, command-and-control traffic, or suspicious domain generation patterns.

This type of automation helps SOC, Threat Hunting, Detection Engineering, Network Security, and Cybersecurity Automation teams identify suspicious DNS activity before it becomes a larger incident.

## Architecture

    +-----------------------------+
    | Domain Inputs                |
    | google.com / github.com      |
    | DGA-like domains             |
    | IP-encoded domains           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | DNS Query Layer              |
    | dig / dnspython              |
    | query_domains.sh             |
    | dns_resolver.py              |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Anomaly Simulation Layer     |
    | dns_anomaly_simulator.py     |
    | - NXDOMAIN events            |
    | - Fast-flux behavior         |
    | - DGA-style domains          |
    | - IP-based domains           |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Detection Engine             |
    | dns_anomaly_detector.py      |
    | - Length analysis            |
    | - Shannon entropy            |
    | - Numeric ratio checks       |
    | - IP-encoded pattern checks  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Security Outputs             |
    | dns_queries.log              |
    | dns_anomaly_events.json      |
    | dns_detection_report.json    |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python virtual environments
- Python pip
- dnspython
- dnsutils
- bind9-host
- dig
- host
- tree
- Git

## Setup & Installation

sudo apt update

sudo apt install -y dnsutils bind9-host python3 python3-pip python3-venv tree git

mkdir -p ~/dns-anomaly-monitor

cd ~/dns-anomaly-monitor

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

pip install dnspython

## How to Reproduce

Run basic DNS CLI checks:

dig +short google.com

dig google.com A +short

dig google.com MX +short

dig google.com NS +short

dig @8.8.8.8 google.com +short

Run the DNS query logger:

./query_domains.sh

cat dns_queries.log

Run the Python DNS resolver:

venv/bin/python dns_resolver.py

venv/bin/python dns_resolver.py google.com github.com example.com --record-type A

Run the DNS anomaly simulator:

venv/bin/python dns_anomaly_simulator.py

Run the DNS anomaly detector:

venv/bin/python dns_anomaly_detector.py

Validate dnspython resolution:

venv/bin/python -c "import dns.resolver; r = dns.resolver.Resolver(); print(r.resolve('google.com', 'A')[0])"

Review generated JSON outputs:

python3 -m json.tool dns_anomaly_events.json

python3 -m json.tool dns_detection_report.json

Verify Python syntax:

venv/bin/python -m py_compile dns_resolver.py dns_anomaly_simulator.py dns_anomaly_detector.py

Review the file tree:

tree .

## Tools Used

- Bash
- Python 3
- dnspython
- dig
- host
- dnsutils
- bind9-host
- JSON
- regular expressions
- Shannon entropy
- Linux
- tree
- Git

## Key Skills Demonstrated

- DNS resolution analysis
- DNS record querying
- Network troubleshooting
- DNS anomaly simulation
- DGA-style domain detection
- Shannon entropy analysis
- Numeric-ratio domain analysis
- IP-encoded domain detection
- Fast-flux behavior simulation
- NXDOMAIN event simulation
- Threat hunting automation
- Detection engineering logic
- SOC workflow support tooling
- JSON security report generation

## Real-World Use Case

Security operations teams can use DNS anomaly detection to identify suspicious network behavior caused by malware, phishing infrastructure, command-and-control communication, or automated domain generation. For example, if an endpoint begins querying many random-looking domains with high entropy, frequent NXDOMAIN responses, or IP-encoded domain patterns, this may indicate compromised host activity. A production-grade version of this toolkit could process DNS logs from SIEM, EDR, DNS resolvers, or cloud logging pipelines and enrich alerts with risk scores for suspicious domains.

## Lessons Learned

- DNS is a valuable signal source for threat hunting because many attacks depend on domain resolution.
- DGA-style domains often look random, long, or high-entropy compared with normal human-readable domains.
- Shannon entropy must be calculated with logarithms; incorrect math can break anomaly detection.
- Fast-flux DNS behavior can be simulated by returning rapidly changing IP sets for the same domain.
- JSON outputs make DNS detection results easier to integrate into SIEM pipelines, dashboards, or automated response workflows.

## Troubleshooting Log

Issue:
Global pip installation can fail or create dependency hygiene problems on Ubuntu 24.04.

Resolution:
Created a Python virtual environment and installed dnspython inside the isolated environment.

Issue:
The original entropy calculation attempted to call bit_length on a float probability value.

Resolution:
Replaced the incorrect logic with proper Shannon entropy calculation using math.log2.

Issue:
The original anomaly simulator printed simulated events but did not save structured artifacts.

Resolution:
Added dns_anomaly_events.json so simulated anomalies can be reviewed, parsed, or integrated with other automation.

Issue:
The original detector only printed console output.

Resolution:
Added dns_detection_report.json for machine-readable risk scoring and detection results.

Issue:
DNS query commands may fail if DNS utilities are missing.

Resolution:
Installed dnsutils and bind9-host, then verified dig and host availability before running DNS checks.
