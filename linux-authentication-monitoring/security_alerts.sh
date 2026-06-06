#!/bin/bash
# Security Alert Analyzer
# Detects suspicious SSH authentication patterns.

LOGFILE=${1:-/var/log/auth.log}
THRESHOLD=5

echo "=== SECURITY ALERTS ==="
echo "Log File: $LOGFILE"
echo "Generated: $(date)"
echo ""

if [ ! -f "$LOGFILE" ]; then
    echo "Log file not found: $LOGFILE"
    exit 1
fi

FAILED_LINES=$(sudo awk '/sshd/ && /Failed password/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")
INVALID_LINES=$(sudo awk '/sshd/ && /Invalid user/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")
SUCCESS_LINES=$(sudo awk '/sshd/ && /Accepted/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")
ROOT_FAILED=$(sudo awk '/sshd/ && /Failed password for root/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")

echo "[ALERT] IPs with more than $THRESHOLD failed attempts:"
echo "$FAILED_LINES" | awk '
{
    for (i=1; i<=NF; i++) {
        if ($i == "from") {
            print $(i+1)
        }
    }
}' | sort | uniq -c | sort -rn | awk -v t="$THRESHOLD" '$1 > t {print $1, "attempts from", $2}'

echo ""

echo "[ALERT] Invalid user login attempts:"
if [ -n "$INVALID_LINES" ]; then
    echo "$INVALID_LINES" | wc -l
    echo "Top targeted invalid usernames:"
    echo "$INVALID_LINES" | awk '
    {
        for (i=1; i<=NF; i++) {
            if ($i == "Invalid" && $(i+1) == "user") {
                print $(i+2)
            }
        }
    }' | sort | uniq -c | sort -rn | head -5
else
    echo "Total: 0"
fi

echo ""

echo "[ALERT] Root login attempts:"
if [ -n "$ROOT_FAILED" ]; then
    echo "$ROOT_FAILED" | wc -l
else
    echo "Failed root attempts: 0"
fi

echo ""

echo "[ALERT] IPs with both failed and successful SSH logins:"
FAILED_IPS=$(echo "$FAILED_LINES" | awk '
{
    for (i=1; i<=NF; i++) {
        if ($i == "from") {
            print $(i+1)
        }
    }
}' | sort -u)

FOUND_MATCH=0

for ip in $FAILED_IPS; do
    SUCCESS=$(echo "$SUCCESS_LINES" | grep -F "$ip" | wc -l)
    if [ "$SUCCESS" -gt 0 ]; then
        echo "IP $ip: Had failures but eventually succeeded"
        FOUND_MATCH=1
    fi
done

if [ "$FOUND_MATCH" -eq 0 ]; then
    echo "No IPs found with both failed and successful SSH authentication."
fi

echo ""
echo "=== END OF REPORT ==="
