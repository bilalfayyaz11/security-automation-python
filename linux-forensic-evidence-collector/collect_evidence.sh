#!/bin/bash

set -euo pipefail

# Automated Evidence Collection Script
# Purpose: Collect Linux system evidence with timestamps, logs, hashes, and summary metadata.

CASE_NAME="linux-forensic-evidence-collection"
COLLECTOR="Bilal_Fayyaz_$(whoami)"
BASE_DIR="$HOME/evidence-collection"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
EVIDENCE_DIR="$BASE_DIR/evidence_$TIMESTAMP"

mkdir -p "$EVIDENCE_DIR"
mkdir -p "$EVIDENCE_DIR/logs"

echo "Evidence collection started..."

cat > "$EVIDENCE_DIR/case_info.txt" << CASEEOF
Case Name: $CASE_NAME
Collector: $COLLECTOR
Collection Start Time: $(date -Iseconds)
Hostname: $(hostname)
Working Directory: $(pwd)
Evidence Directory: $EVIDENCE_DIR
CASEEOF

collect_system_info() {
    echo "Collecting system information..."

    hostname > "$EVIDENCE_DIR/hostname.txt"
    uptime > "$EVIDENCE_DIR/uptime.txt"
    cat /etc/os-release > "$EVIDENCE_DIR/os_info.txt"
    uname -a > "$EVIDENCE_DIR/kernel_info.txt"
    date -Iseconds > "$EVIDENCE_DIR/collection_time.txt"
    whoami > "$EVIDENCE_DIR/executed_by.txt"
}

collect_user_process_info() {
    echo "Collecting user and process information..."

    w > "$EVIDENCE_DIR/logged_users.txt" || true
    cat /etc/passwd > "$EVIDENCE_DIR/user_accounts.txt"
    ps aux > "$EVIDENCE_DIR/running_processes.txt"
    last > "$EVIDENCE_DIR/last_logins.txt" || true
    sudo lastb > "$EVIDENCE_DIR/failed_logins.txt" 2>/dev/null || echo "failed login database not available or permission denied" > "$EVIDENCE_DIR/failed_logins.txt"
}

collect_network_info() {
    echo "Collecting network information..."

    ip addr > "$EVIDENCE_DIR/network_interfaces.txt"
    ip route > "$EVIDENCE_DIR/routing_table.txt"

    if command -v ss >/dev/null 2>&1; then
        ss -tuln > "$EVIDENCE_DIR/network_connections.txt"
    elif command -v netstat >/dev/null 2>&1; then
        netstat -tuln > "$EVIDENCE_DIR/network_connections.txt"
    else
        echo "Neither ss nor netstat is available" > "$EVIDENCE_DIR/network_connections.txt"
    fi
}

collect_logs() {
    echo "Collecting system logs..."

    sudo cp /var/log/auth.log* "$EVIDENCE_DIR/logs/" 2>/dev/null || true
    sudo cp /var/log/syslog* "$EVIDENCE_DIR/logs/" 2>/dev/null || true
    sudo cp /var/log/kern.log* "$EVIDENCE_DIR/logs/" 2>/dev/null || true

    if command -v journalctl >/dev/null 2>&1; then
        sudo journalctl --no-pager > "$EVIDENCE_DIR/logs/journal.log" 2>/dev/null || true
    fi
}

create_hashes() {
    echo "Creating hash values for evidence integrity..."

    find "$EVIDENCE_DIR" -type f ! -name "evidence_md5.txt" ! -name "evidence_sha256.txt" -exec md5sum {} \; > "$EVIDENCE_DIR/evidence_md5.txt"
    find "$EVIDENCE_DIR" -type f ! -name "evidence_md5.txt" ! -name "evidence_sha256.txt" -exec sha256sum {} \; > "$EVIDENCE_DIR/evidence_sha256.txt"
}

create_summary() {
    echo "Creating collection summary..."

    cat > "$EVIDENCE_DIR/collection_summary.txt" << SUMMARYEOF
Collection End Time: $(date -Iseconds)
Evidence Directory: $EVIDENCE_DIR
Total Files Collected: $(find "$EVIDENCE_DIR" -type f | wc -l)
Evidence Directory Size: $(du -sh "$EVIDENCE_DIR" | awk '{print $1}')
Hash Files:
- evidence_md5.txt
- evidence_sha256.txt
SUMMARYEOF
}

collect_system_info
collect_user_process_info
collect_network_info
collect_logs
create_hashes
create_summary

echo "Evidence collection completed!"
echo "Evidence stored in: $EVIDENCE_DIR"
