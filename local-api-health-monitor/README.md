# Local API Health Monitor

## What This Does

This implementation provides a local API health monitoring system built with Python and Flask. It creates a mock API service with multiple endpoints, checks endpoint availability, measures response times, detects HTTP failures, logs health status over time, and writes the latest service state to a structured JSON status file.

The monitor simulates real production behavior by including healthy endpoints, slow responses, and intermittent failures. This makes it useful for testing monitoring logic, incident detection workflows, service reliability checks, and basic AIOps-style health analysis.

This type of automation helps SRE, DevOps, Platform Engineering, Cloud Operations, and AIOps teams detect service degradation before users report outages.

## Architecture

    +-----------------------------+
    | Mock API Service             |
    | Flask / localhost:5000       |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | API Endpoints                |
    | /health                     |
    | /api/users                  |
    | /api/data                   |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Health Monitor               |
    | health_monitor.py            |
    | - HTTP checks                |
    | - Response timing            |
    | - Failure detection          |
    | - Status classification      |
    +-------------+---------------+
                  |
                  v
    +-----------------------------+
    | Observability Output         |
    | logs/health_monitor.log      |
    | logs/current_status.json     |
    | logs/api_server.log          |
    +-----------------------------+

## Prerequisites

- Ubuntu 24.04
- Python 3
- Python virtual environments
- Python pip
- Flask
- Requests
- curl
- jq
- lsof
- tree
- Git

## Setup & Installation

sudo apt update

sudo apt install -y python3 python3-pip python3-venv curl jq lsof tree git

mkdir -p ~/api-health-monitor

cd ~/api-health-monitor

python3 -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip

pip install flask requests

## How to Reproduce

Start the mock API service:

source venv/bin/activate

nohup venv/bin/python mock-api/api_server.py > logs/api_server.log 2>&1 &

echo $! > api_pid.txt

sleep 3

Verify the mock API endpoints:

curl -s http://localhost:5000/health | python3 -m json.tool

curl -s http://localhost:5000/api/users | python3 -m json.tool

curl -s http://localhost:5000/api/data | python3 -m json.tool

Run the health monitor:

venv/bin/python health_monitor.py --interval 3 --duration 35

View health logs:

cat logs/health_monitor.log

View current service status:

cat logs/current_status.json | python3 -m json.tool

Count healthy checks:

grep "is healthy" logs/health_monitor.log | wc -l

Count unhealthy checks:

grep -E "is unhealthy|is error|is timeout|is unreachable" logs/health_monitor.log | wc -l

View detected errors:

grep "\[ERROR\]" logs/health_monitor.log

View response-time snapshot:

cat logs/current_status.json | jq '.endpoints[] | {endpoint: .endpoint, status: .status, response_time_ms: .response_time_ms}'

Stop the mock API:

kill "$(cat api_pid.txt)"

## Tools Used

- Python 3
- Flask
- Requests
- Bash
- curl
- jq
- lsof
- JSON
- Linux process management
- nohup
- tree
- Git

## Key Skills Demonstrated

- API health monitoring
- Endpoint availability checks
- HTTP status code validation
- Response-time measurement
- Structured logging
- JSON status reporting
- Failure detection
- Service degradation simulation
- Background process management
- Local observability workflow design
- SRE-style monitoring automation
- AIOps-ready health signal generation
- Production troubleshooting fundamentals

## Real-World Use Case

A platform engineering or SRE team can use this type of monitor to check whether internal APIs are reachable, healthy, slow, or returning server errors. In a production environment, similar logic can be integrated into synthetic monitoring, uptime checks, CI/CD smoke tests, Kubernetes readiness validation, or incident response workflows. The generated logs and JSON status output can also feed dashboards, alerting systems, or AIOps pipelines for automated service health analysis.

## Lessons Learned

- Health monitoring should check more than whether a service is reachable; it should also measure latency and classify failures.
- Mock services are useful for testing monitoring behavior because they can simulate slow responses and intermittent errors safely.
- Response timing should use time.perf_counter instead of time.time for more accurate latency measurement.
- Background services should be started with clear PID tracking and log redirection.
- JSON status files make monitoring output easier to consume by scripts, dashboards, and automation pipelines.

## Troubleshooting Log

Issue:
Global pip installation can fail or create dependency management problems on Ubuntu 24.04.

Resolution:
Created a Python virtual environment and installed Flask and Requests inside the isolated environment.

Issue:
Starting the API with a simple background ampersand command can leave logs attached to the terminal and make cleanup messy.

Resolution:
Started the Flask API with nohup, redirected output to logs/api_server.log, and stored the process ID in api_pid.txt.

Issue:
Port 5000 may already be in use from a previous service.

Resolution:
Used lsof to detect and terminate existing processes listening on port 5000 before starting the mock API.

Issue:
The original timing logic used time.time for latency measurement.

Resolution:
Updated the monitor to use time.perf_counter for more accurate response-time tracking.

Issue:
The mock API intentionally returns HTTP 500 every fifth user request.

Resolution:
The health monitor correctly classified non-2xx responses as unhealthy and logged them as ERROR events.
