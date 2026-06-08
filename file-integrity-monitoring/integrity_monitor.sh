#!/bin/bash

REPORT_FILE="/var/log/aide_check_$(date +%Y%m%d_%H%M%S).log"
ALERT_FILE="/var/log/aide_alerts.log"
CONFIG_FILE="/etc/aide/aide.conf"

echo "Running integrity check at $(date)" | tee -a "$ALERT_FILE"

aide --config="$CONFIG_FILE" --check > "$REPORT_FILE" 2>&1
AIDE_STATUS=$?

if [ "$AIDE_STATUS" -ne 0 ] || grep -Eiq "added|removed|changed|difference" "$REPORT_FILE"; then
    echo "ALERT: File integrity violations detected!" | tee -a "$ALERT_FILE"
    echo "Report saved to: $REPORT_FILE" | tee -a "$ALERT_FILE"
    grep -A 20 -i "^Summary:" "$REPORT_FILE" | tee -a "$ALERT_FILE" || true
    echo "---" | tee -a "$ALERT_FILE"
else
    echo "No integrity violations detected." | tee -a "$ALERT_FILE"
fi
