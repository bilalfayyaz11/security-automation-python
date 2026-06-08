# Network Metadata Extraction Utility

## What This Does

This implementation provides a Python-based network metadata extraction utility for parsing network traffic logs and producing enriched security intelligence. It extracts timestamps, protocols, source IPs, source ports, destination IPs, and destination ports from structured traffic records, then enriches each connection with service identification, IP classification, traffic direction, and privileged-port context.

The utility converts raw network records into structured JSON that can be reviewed by analysts, integrated into dashboards, or used by downstream security automation. It also generates a console report showing protocol distribution, top services, unique IPs, traffic direction, destination classification, and top destination IPs.

This type of tool is useful for SOC, Network Security, Threat Hunting, Incident Response, DFIR, and Cloud Security teams that need to quickly understand network activity from logs.

## Architecture

    +-----------------------------+
    | Network Traffic Logs         |
    | network_traffic.log          |
    | test_input.log               |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Parsing Layer                |
    | network_metadata_extractor   |
    | - Regex parsing              |
    | - IP validation              |
    | - Port extraction            |
    | - Protocol extraction        |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Enrichment Layer             |
    | - Service mapping            |
    | - IP classification          |
    | - Direction classification   |
    | - Privileged port detection  |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Reporting Layer              |
    | - Console summary            |
    | - JSON metadata export       |
    | - Parse error tracking       |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python virtual environments
- tcpdump
- tshark
- tree
- Git

## Setup & Installation

sudo apt update

sudo DEBIAN_FRONTEND=noninteractive apt install -y python3 python3-pip python3-venv tcpdump tshark tree git

mkdir -p ~/network-metadata-extractor

cd ~/network-metadata-extractor

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

## How to Reproduce

Run the main extractor against the included traffic log:

venv/bin/python network_metadata_extractor.py --input network_traffic.log --output network_metadata.json

Review the generated JSON output:

python3 -m json.tool network_metadata.json

Count extracted connections and services:

python3 << 'PY'
import json

with open("network_metadata.json", "r", encoding="utf-8") as file:
    data = json.load(file)

services = {}
for record in data["metadata"]:
    services[record["service"]] = services.get(record["service"], 0) + 1

print(f"Total connections extracted: {len(data['metadata'])}")
print(f"Unique services identified: {len(services)}")
for service, count in sorted(services.items(), key=lambda item: item[1], reverse=True):
    print(f"{service}: {count}")
PY

Run the extractor against the custom test input:

venv/bin/python network_metadata_extractor.py --input test_input.log --output test_network_metadata.json

Review custom output:

python3 -m json.tool test_network_metadata.json

Optional live packet capture:

sudo timeout 10 tcpdump -i any -c 20 -w capture.pcap 2>/dev/null

tshark -r capture.pcap -T fields -e frame.time -e ip.proto -e ip.src -e tcp.srcport -e udp.srcport -e ip.dst -e tcp.dstport -e udp.dstport 2>/dev/null > live_traffic.txt

Verify Python syntax:

venv/bin/python -m py_compile network_metadata_extractor.py

Review file tree:

tree .

## Tools Used

- Python 3
- Bash
- regular expressions
- ipaddress
- JSON
- Counter
- defaultdict
- argparse
- tcpdump
- tshark
- Linux
- tree
- Git

## Key Skills Demonstrated

- Network log parsing
- Metadata extraction
- Traffic enrichment
- IP address validation
- Internal and external traffic classification
- Service identification from destination ports
- Traffic direction classification
- JSON export for automation
- Parse error handling
- Network security analysis
- Incident response data preparation
- Threat hunting workflow support
- SOC automation fundamentals

## Real-World Use Case

A security team can use this utility during incident response or network investigations to convert raw traffic logs into structured metadata. For example, if analysts receive firewall logs, proxy logs, or packet-derived records, this tool can extract connection details, identify common services, classify traffic direction, and export JSON for deeper analysis. A production version could ingest SIEM exports, cloud flow logs, packet metadata, or EDR network telemetry and feed enriched results into detection pipelines.

## Lessons Learned

- Raw network logs become much more useful when enriched with service names and traffic direction.
- Manual private-IP checks are fragile; Python’s ipaddress module is safer and handles more address categories.
- Structured JSON export makes network metadata easier to reuse in automation, dashboards, and security tools.
- CLI arguments make the utility reusable across multiple input files instead of hardcoding one log file.
- Tracking parse errors helps analysts identify malformed or unsupported log formats instead of silently losing data.

## Troubleshooting Log

Issue:
The original IP classification logic manually checked only common private ranges.

Resolution:
Replaced manual range checks with Python’s ipaddress module to classify private, loopback, multicast, reserved, and external addresses more reliably.

Issue:
The original script hardcoded network_traffic.log as the only input source.

Resolution:
Added --input and --output CLI arguments so the extractor can process different traffic files and write separate JSON outputs.

Issue:
The original workflow referenced optional GeoIP packages that may not install reliably in a fresh Ubuntu 24.04 environment.

Resolution:
Removed dependency on unreliable optional GeoIP packages and focused the implementation on deterministic service and IP metadata enrichment.

Issue:
Global pip installation can fail or create dependency hygiene issues on Ubuntu 24.04.

Resolution:
Created a Python virtual environment and kept execution isolated.

Issue:
Packet capture tools may prompt during tshark installation.

Resolution:
Used DEBIAN_FRONTEND=noninteractive during package installation to prevent interactive prompts from blocking execution.
