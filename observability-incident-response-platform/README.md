# Observability and Incident Response Platform

## What This Does

This implementation provides a complete observability and incident response platform using Prometheus, Grafana, Loki, Promtail, Node Exporter, and a monitored Flask application.

The system collects infrastructure metrics, application metrics, service health data, and centralized logs. It also defines alert rules for high CPU usage, high memory usage, and low disk space while providing incident simulation scripts to validate operational readiness.

This type of platform is used by DevOps, SRE, Platform Engineering, Cloud Engineering, and AIOps teams to detect failures faster, investigate incidents with evidence, and reduce mean time to resolution.

## Architecture

    +------------------------------------------------+
    | Linux Host                                     |
    | Ubuntu 24.04                                  |
    +-----------------------+------------------------+
                            |
                            v
    +------------------------------------------------+
    | System Metrics Layer                           |
    | Node Exporter :9100                            |
    | CPU, Memory, Disk, Filesystem Metrics          |
    +-----------------------+------------------------+
                            |
                            v
    +------------------------------------------------+
    | Application Layer                              |
    | Flask Monitor App :8080                        |
    | /, /health, /load, /metrics                    |
    | App Logs: ~/observability-lab/app.log          |
    +-----------------------+------------------------+
                            |
              +-------------+-------------+
              |                           |
              v                           v
    +-----------------------------+   +-----------------------------+
    | Metrics Collection          |   | Log Collection              |
    | Prometheus :9090            |   | Promtail :9080              |
    | Scrapes Node Exporter       |   | Ships App/System Logs       |
    | Scrapes Flask Metrics       |   +-------------+---------------+
    | Evaluates Alert Rules       |                 |
    +-------------+---------------+                 v
                  |                   +-----------------------------+
                  |                   | Log Storage                 |
                  |                   | Loki :3100                  |
                  |                   | Centralized Log Queries     |
                  |                   +-------------+---------------+
                  |                                 |
                  +----------------+----------------+
                                   |
                                   v
    +------------------------------------------------+
    | Visualization and Investigation Layer          |
    | Grafana :3000                                  |
    | Prometheus Data Source                         |
    | Loki Data Source                               |
    +-----------------------+------------------------+
                            |
                            v
    +------------------------------------------------+
    | Incident Response Workflow                     |
    | generate_traffic.sh                            |
    | simulate_incident.sh                           |
    | verify_ir.sh                                   |
    | incident_response.md                           |
    +------------------------------------------------+

## Prerequisites

- Ubuntu 24.04
- systemd
- Git
- curl
- wget
- tar
- unzip
- jq
- Python 3
- Python virtual environments
- pip
- net-tools
- stress-ng
- apache2-utils
- Prometheus
- Node Exporter
- Grafana
- Loki
- Promtail

## Setup & Installation

sudo apt update

sudo apt install -y wget curl tar git stress-ng apache2-utils unzip jq python3 python3-pip python3-venv net-tools software-properties-common apt-transport-https gpg

mkdir -p ~/observability-lab

cd ~/observability-lab

wget -q https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-amd64.tar.gz

tar xzf prometheus-2.47.0.linux-amd64.tar.gz

sudo mv prometheus-2.47.0.linux-amd64 /opt/prometheus

sudo id prometheus >/dev/null 2>&1 || sudo useradd --no-create-home --shell /bin/false prometheus

sudo mkdir -p /opt/prometheus/data

sudo chown -R prometheus:prometheus /opt/prometheus

wget -q https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz

tar xzf node_exporter-1.6.1.linux-amd64.tar.gz

sudo mv node_exporter-1.6.1.linux-amd64/node_exporter /usr/local/bin/

sudo chmod +x /usr/local/bin/node_exporter

curl -fsSL https://apt.grafana.com/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/grafana.gpg

echo "deb [signed-by=/usr/share/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt update

sudo apt install -y grafana

wget -q https://github.com/grafana/loki/releases/download/v2.9.1/loki-linux-amd64.zip

unzip -o loki-linux-amd64.zip

sudo mv loki-linux-amd64 /usr/local/bin/loki

sudo chmod +x /usr/local/bin/loki

wget -q https://github.com/grafana/loki/releases/download/v2.9.1/promtail-linux-amd64.zip

unzip -o promtail-linux-amd64.zip

sudo mv promtail-linux-amd64 /usr/local/bin/promtail

sudo chmod +x /usr/local/bin/promtail

python3 -m venv ~/observability-lab/venv

source ~/observability-lab/venv/bin/activate

pip install --upgrade pip

pip install flask prometheus_client

## How to Reproduce

Start and verify the observability services:

systemctl is-active prometheus node_exporter loki promtail grafana-server monitor-app

Check listening ports:

sudo netstat -tlnp | grep -E '9090|9100|3100|9080|3000|8080'

Check Prometheus readiness:

curl -s http://localhost:9090/-/ready

Check Loki readiness:

curl -s http://localhost:3100/ready

Check Grafana health:

curl -s http://localhost:3000/api/health | jq

Generate normal traffic:

./generate_traffic.sh

Run incident simulation:

./simulate_incident.sh

Run final verification:

./verify_ir.sh

Query Prometheus targets:

curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'

Query collected metrics:

curl -s 'http://localhost:9090/api/v1/query?query=up' | jq

Query active alerts:

curl -s http://localhost:9090/api/v1/alerts | jq

Query Loki log sources:

curl -s "http://localhost:3100/loki/api/v1/label/job/values" | jq

Query application logs from Loki:

curl -s "http://localhost:3100/loki/api/v1/query_range?query={job=\"application\"}&limit=5" | jq

View local application logs:

tail -n 50 ~/observability-lab/app.log

## Tools Used

- Prometheus
- Node Exporter
- Grafana
- Loki
- Promtail
- Flask
- prometheus_client
- Python 3
- Bash
- systemd
- jq
- curl
- wget
- stress-ng
- net-tools
- Ubuntu 24.04

## Key Skills Demonstrated

- Observability platform deployment
- Metrics collection with Prometheus
- Infrastructure monitoring with Node Exporter
- Application metrics instrumentation
- Centralized log aggregation with Loki and Promtail
- Grafana data source configuration
- Alert rule configuration
- Incident response simulation
- Service health validation
- Linux service management with systemd
- Troubleshooting distributed monitoring components
- AIOps-style operational readiness testing
- SRE incident investigation workflow

## Real-World Use Case

Production engineering teams need visibility into system health, application behavior, logs, and failure patterns before outages become business-impacting incidents. This platform demonstrates how an organization can monitor Linux infrastructure, collect custom application metrics, aggregate logs centrally, configure alerting rules, and run controlled incident simulations to validate operational response. Similar patterns are used in cloud platforms, Kubernetes clusters, internal developer platforms, SaaS systems, and enterprise reliability programs.

## Lessons Learned

- Observability requires metrics, logs, alerts, and repeatable investigation workflows working together.
- Prometheus is effective for time-series metrics and alert evaluation, while Loki provides lightweight centralized log querying.
- Application instrumentation improves incident diagnosis because service behavior becomes measurable.
- Incident drills are necessary because monitoring systems must be validated before real outages happen.
- Service readiness checks are critical because active systemd status does not always mean an API is immediately ready.

## Troubleshooting Log

Issue:
The Grafana repository setup used apt-key, which is deprecated on Ubuntu 24.04.

Resolution:
Configured the Grafana repository using a signed keyring under /usr/share/keyrings/grafana.gpg.

Issue:
The original instructions used unzip for Loki and Promtail but did not install unzip.

Resolution:
Installed unzip as part of the base dependency block before extracting Loki and Promtail.

Issue:
Loki initially reported that the ingester was not ready.

Resolution:
Waited for Loki readiness before continuing because Loki requires a short startup period after service activation.

Issue:
The original Loki configuration used older storage configuration patterns.

Resolution:
Used a Loki 2.9-compatible common configuration with filesystem storage and boltdb-shipper indexing.

Issue:
The starter Flask application referenced os.environ but the initial incomplete code did not import os.

Resolution:
Used the completed implementation and explicitly imported os.

Issue:
Global pip installation can fail on Ubuntu 24.04 due to externally managed Python environments.

Resolution:
Created a Python virtual environment and installed Flask plus prometheus_client inside the virtual environment.

Issue:
The troubleshooting command referenced promtail under the Prometheus directory for Prometheus config checking.

Resolution:
Validated Prometheus using /opt/prometheus/promtool check config /opt/prometheus/prometheus.yml.

Issue:
Prometheus needed the monitored application endpoint to be available on port 8080.

Resolution:
Created and enabled monitor-app.service using the virtual environment Python interpreter.
