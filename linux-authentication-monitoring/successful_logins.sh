#!/bin/bash
# Successful Login Analyzer
# Reports real SSH successful authentication events.

LOGFILE=${1:-/var/log/auth.log}

echo "=== Successful Login Report ==="
echo "Log File: $LOGFILE"
echo "Generated: $(date)"
echo ""

if [ ! -f "$LOGFILE" ]; then
    echo "Log file not found: $LOGFILE"
    exit 1
fi

SUCCESS_LINES=$(sudo awk '/sshd/ && /Accepted/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")

echo "Total Successful SSH Logins:"
if [ -n "$SUCCESS_LINES" ]; then
    echo "$SUCCESS_LINES" | grep -c "Accepted"
else
    echo 0
fi

echo ""
echo "Users Who Logged In:"
echo "$SUCCESS_LINES" | awk '
{
    for (i=1; i<=NF; i++) {
        if ($i == "for") {
            print $(i+1)
        }
    }
}' | sort -u

echo ""
echo "Recent 10 Successful SSH Logins:"
if [ -n "$SUCCESS_LINES" ]; then
    echo "$SUCCESS_LINES" | tail -10 | awk '
    {
        user="-"
        ip="-"
        method="-"

        for (i=1; i<=NF; i++) {
            if ($i == "Accepted") {
                method=$(i+1)
            }
            if ($i == "for") {
                user=$(i+1)
            }
            if ($i == "from") {
                ip=$(i+1)
            }
        }

        print $1, "-", method, "login for", user, "from", ip
    }'
else
    echo "No real successful SSH login events found."
fi
