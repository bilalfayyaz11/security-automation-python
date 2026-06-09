#!/bin/bash
set -euo pipefail

echo "Generating normal application traffic..."

for i in {1..50}; do
  curl -s http://localhost:8080/ > /dev/null
  curl -s http://localhost:8080/health > /dev/null || true
  sleep 0.5
done

echo "Traffic generation complete"
