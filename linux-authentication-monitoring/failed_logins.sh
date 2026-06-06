#!/bin/bash
# Failed Login Analyzer
# Reports real SSH failed-password authentication attempts only.

LOGFILE=${1:-/var/log/auth.log}

echo "=== Failed Login Attempts Report ==="
echo "Log File: $LOGFILE"
echo "Generated: $(date)"
echo ""

if [ ! -f "$LOGFILE" ]; then
    echo "Log file not found: $LOGFILE"
    exit 1
fi

FAILED_LINES=$(sudo awk '/sshd/ && /Failed password/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")

echo "Total Failed Attempts:"
if [ -n "$FAILED_LINES" ]; then
    echo "$FAILED_LINES" | grep -c "Failed password"
else
    echo 0
fi

echo ""
echo "Top 10 Usernames Targeted:"
echo "$FAILED_LINES" | awk '
{
    for (i=1; i<=NF; i++) {
        if ($i == "for" && $(i+1) == "invalid" && $(i+2) == "user") {
            print $(i+3)
        } else if ($i == "for" && $(i+1) != "invalid") {
            print $(i+1)
        }
    }
}' | sort | uniq -c | sort -rn | head -10

echo ""
echo "Top 10 Source IPs:"
echo "$FAILED_LINES" | awk '
{
    for (i=1; i<=NF; i++) {
        if ($i == "from") {
            print $(i+1)
        }
    }
}' | sort | uniq -c | sort -rn | head -10

echo ""
echo "Raw failed SSH events:"
if [ -n "$FAILED_LINES" ]; then
    echo "$FAILED_LINES" | tail -5
else
    echo "No real sshd failed-password events found."
fi
