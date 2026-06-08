#!/bin/bash

set -euo pipefail

DOMAINS=("google.com" "github.com" "stackoverflow.com" "example.com")
LOGFILE="dns_queries.log"

echo "=== DNS Query Log - $(date -Iseconds) ===" >> "$LOGFILE"

for domain in "${DOMAINS[@]}"; do
    echo "Querying: $domain" >> "$LOGFILE"
    dig +short "$domain" >> "$LOGFILE" || echo "DNS query failed for $domain" >> "$LOGFILE"
    echo "---" >> "$LOGFILE"
done
