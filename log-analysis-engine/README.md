
# Log Analysis Engine

## What This Does

This implementation provides a structured log analysis engine capable of parsing application and infrastructure logs into machine-readable data. The system extracts timestamps, IP addresses, severity levels, and message content, enabling downstream analysis and automation.

The platform supports log tokenization, IPv4 validation, severity-based filtering, statistical reporting, keyword search, and CSV export functionality. These capabilities form the foundation of many observability, security monitoring, SIEM, SOC, and AIOps workflows.

By converting raw log data into structured records, engineers can automate troubleshooting, accelerate incident response, and generate actionable operational insights.

## Architecture

```
+----------------------------+
| Raw Log Files              |
| sample.log                 |
+-------------+--------------+
              |
              v
+----------------------------+
| Log Parsing Engine         |
| log_parser.py              |
| Regex Processing           |
| Timestamp Extraction       |
| IPv4 Validation            |
+-------------+--------------+
              |
              v
+----------------------------+
| Analysis Layer             |
| Tokenization               |
| Severity Filtering         |
| Search Engine              |
| Statistics Generation      |
+-------------+--------------+
              |
              v
+----------------------------+
| Export Layer               |
| output.csv                 |
| Structured Reports         |
+----------------------------+
```

## Prerequisites

* Ubuntu 24.04
* Python 3.12+
* python3-pip
* Git
* tree

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv git tree

mkdir -p ~/log-analysis-engine

cd ~/log-analysis-engine

## How to Reproduce

Create sample log data:

cat sample.log

Run the parser:

python3 log_parser.py

Run advanced analytics:

python3 advanced_parser.py

Verify CSV export:

cat output.csv

Run validation tests:

python3 -c "
from log_parser import validate_ip_address
print(validate_ip_address('192.168.1.100'))
"

View generated files:

tree -a .

## Features Implemented

* Structured log parsing
* Timestamp extraction
* IPv4 validation
* Message tokenization
* Severity filtering
* Log searching
* Statistical analysis
* Top IP detection
* CSV export
* Structured reporting

## Tools Used

* Python 3
* Regular Expressions (re)
* CSV Module
* Collections Counter
* Datetime Module
* Linux
* Git
* Bash

## Key Skills Demonstrated

* Log analysis automation
* Python scripting
* Regex pattern matching
* Security event processing
* Data extraction and normalization
* Structured data transformation
* Statistical reporting
* CSV generation
* Defensive input validation
* Operational troubleshooting automation

## Real-World Use Case

Modern engineering organizations generate massive volumes of application, infrastructure, cloud, and security logs. Engineers often need to identify authentication failures, service outages, abnormal behavior, and operational issues quickly. This solution provides the foundational capabilities used by SIEM platforms, SOC tooling, observability pipelines, security monitoring systems, and AIOps platforms to transform raw log data into actionable information.

## Lessons Learned

* Well-designed regex patterns dramatically improve parsing reliability.
* Input validation prevents malformed log entries from polluting datasets.
* Tokenization enables future search and analytics capabilities.
* Structured exports make integration with reporting tools easier.
* Separating parsing and analytics logic improves maintainability.

## Troubleshooting Log

Issue:
Ubuntu 24.04 environment did not include pip3.

Resolution:
Installed python3-pip using apt.

Issue:
Ubuntu 24.04 environment did not include tree.

Resolution:
Installed tree using apt.

Issue:
Starter implementation contained multiple unfinished TODO sections.

Resolution:
Implemented all parsing, validation, filtering, tokenization, and export functions.

Issue:
Generic regex patterns can accidentally match malformed entries.

Resolution:
Added structured matching and IPv4 validation before accepting parsed records.

Issue:
Exported data required interoperability with external tooling.

Resolution:
Implemented CSV export for structured downstream consumption.
