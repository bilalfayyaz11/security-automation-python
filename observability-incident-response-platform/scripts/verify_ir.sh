#!/bin/bash
set -euo pipefail

echo "=== Incident Response Verification ==="
echo ""

echo "Test 1: Checking alert rules..."
RULES=$(curl -s http://localhost:9090/api/v1/rules | jq '[.data.groups[].rules[]] | length')
if [ "$RULES" -gt 0 ]; then
  echo "✓ Alert rules loaded: $RULES rules found"
else
  echo "✗ No alert rules found"
fi

echo ""
echo "Test 2: Verifying metrics collection..."
METRICS=$(curl -s http://localhost:9090/api/v1/label/__name__/values | jq '.data | length')
if [ "$METRICS" -gt 10 ]; then
  echo "✓ Metrics being collected: $METRICS unique metrics"
else
  echo "✗ Insufficient metrics"
fi

echo ""
echo "Test 3: Checking log aggregation..."
LOGS=$(curl -s "http://localhost:3100/loki/api/v1/label/job/values" | jq '.data | length')
if [ "$LOGS" -gt 0 ]; then
  echo "✓ Logs being aggregated: $LOGS log sources"
else
  echo "✗ No logs found"
fi

echo ""
echo "Test 4: Testing application..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/)
if [ "$HTTP_CODE" -eq 200 ]; then
  echo "✓ Application responding correctly"
else
  echo "✗ Application not responding. HTTP $HTTP_CODE"
fi

echo ""
echo "=== Verification Complete ==="
