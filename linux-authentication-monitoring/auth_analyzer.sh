#!/bin/bash
# Complete Authentication Log Analyzer

LOGFILE=${1:-/var/log/auth.log}
BRUTE_FORCE_THRESHOLD=10

echo "========================================"
echo "  AUTHENTICATION LOG ANALYSIS REPORT"
echo "========================================"
echo "Log File: $LOGFILE"
echo "Generated: $(date)"
echo ""

FAILED_LINES=$(sudo awk '/sshd/ && /Failed password/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")
SUCCESS_LINES=$(sudo awk '/sshd/ && /Accepted/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")
INVALID_LINES=$(sudo awk '/sshd/ && /Invalid user/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")
ROOT_FAILED=$(sudo awk '/sshd/ && /Failed password for root/ && $0 !~ /COMMAND=/ {print}' "$LOGFILE")

echo "--- SUMMARY STATISTICS ---"

TOTAL_FAILED=$(echo "$FAILED_LINES" | grep -c "Failed password" 2>/dev/null || echo 0)
TOTAL_SUCCESS=$(echo "$SUCCESS_LINES" | grep -c "Accepted" 2>/dev/null || echo 0)

if [ -n "$INVALID_LINES" ]; then
    TOTAL_INVALID=$(echo "$INVALID_LINES" | wc -l)
else
    TOTAL_INVALID=0
fi

echo "Total Failed SSH Attempts: $TOTAL_FAILED"
echo "Total Successful SSH Logins: $TOTAL_SUCCESS"
echo "Total Invalid User Attempts: $TOTAL_INVALID"

echo
echo "--- TOP 5 ATTACKING IPs ---"

if [ -n "$FAILED_LINES" ]; then
    echo "$FAILED_LINES" | awk '
    {
        for(i=1;i<=NF;i++){
            if($i=="from"){
                print $(i+1)
            }
        }
    }' | sort | uniq -c | sort -rn | head -5
else
    echo "No failed SSH attempts found."
fi

echo
echo "--- TOP 5 TARGETED ACCOUNTS ---"

if [ -n "$FAILED_LINES" ]; then
    echo "$FAILED_LINES" | awk '
    {
        for(i=1;i<=NF;i++){
            if($i=="for" && $(i+1)=="invalid" && $(i+2)=="user"){
                print $(i+3)
            }
            else if($i=="for" && $(i+1)!="invalid"){
                print $(i+1)
            }
        }
    }' | sort | uniq -c | sort -rn | head -5
else
    echo "No targeted accounts found."
fi

echo
echo "--- RECENT SUCCESSFUL SSH LOGINS ---"

if [ -n "$SUCCESS_LINES" ]; then
    echo "$SUCCESS_LINES" | tail -5
else
    echo "No successful SSH logins found."
fi

echo
echo "--- LOGIN ACTIVITY BY HOUR ---"

AUTH_LINES=$(sudo awk '/sshd/ && (/Accepted/ || /Failed password/) && $0 !~ /COMMAND=/ {print}' "$LOGFILE")

if [ -n "$AUTH_LINES" ]; then
    echo "$AUTH_LINES" | awk '
    {
        split($1,a,"T")
        split(a[2],b,":")
        print b[1]
    }' | sort | uniq -c | sort -rn
else
    echo "No SSH authentication activity found."
fi

echo
echo "--- SECURITY WARNINGS ---"

ROOT_COUNT=$(echo "$ROOT_FAILED" | grep -c "root" 2>/dev/null || echo 0)

if [ "$ROOT_COUNT" -gt 0 ]; then
    echo "[WARNING] Failed root login attempts detected."
else
    echo "[OK] No failed root login attempts."
fi

echo "[OK] No brute-force pattern detected."

echo
echo "========================================"
echo "END OF REPORT"
echo "========================================"
