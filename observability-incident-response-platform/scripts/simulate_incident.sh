#!/bin/bash
set -euo pipefail

echo "=== Starting Incident Response Drill ==="
echo ""

echo "[INCIDENT 1] Simulating high CPU usage..."
stress-ng --cpu 4 --timeout 90s --quiet &
STRESS_PID=$!

echo "CPU stress test running. PID: $STRESS_PID"
echo "Prometheus alerts endpoint: http://localhost:9090/alerts"
echo "Waiting 90 seconds for alert evaluation..."
sleep 90

echo ""
echo "[RESOLUTION 1] CPU stress test completed"
echo ""

echo "[INCIDENT 2] Generating application health-check errors..."
for i in {1..100}; do
  curl -s http://localhost:8080/health > /dev/null || true
  sleep 0.1
done

echo "Application errors generated."
echo ""

echo "[INCIDENT 3] Simulating memory pressure..."
stress-ng --vm 2 --vm-bytes 512M --timeout 60s --quiet &
MEM_PID=$!

echo "Memory stress test running. PID: $MEM_PID"
sleep 60

echo ""
echo "=== Incident Response Drill Complete ==="
echo "Review:"
echo "1. Prometheus alerts: http://localhost:9090/alerts"
echo "2. Grafana dashboards: http://localhost:3000"
echo "3. Application logs: tail ~/observability-lab/app.log"
echo "4. Service logs: journalctl -u monitor-app -n 50"
