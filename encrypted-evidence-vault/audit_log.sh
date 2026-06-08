#!/bin/bash

LOG_FILE="$HOME/evidence-lab/vault_audit.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
USER_NAME=$(whoami)
ACTION="$1"
DETAILS="$2"

echo "[$TIMESTAMP] USER:$USER_NAME ACTION:$ACTION DETAILS:$DETAILS" >> "$LOG_FILE"

echo "Audit entry logged"
