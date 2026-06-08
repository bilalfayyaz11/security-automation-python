#!/bin/bash

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 /path/to/evidence_directory"
    exit 1
fi

EVIDENCE_DIR="$1"

if [ ! -d "$EVIDENCE_DIR" ]; then
    echo "ERROR: Evidence directory does not exist: $EVIDENCE_DIR"
    exit 1
fi

echo "Starting evidence verification..."
echo "Evidence directory: $EVIDENCE_DIR"

echo
echo "===== MD5 VERIFICATION ====="
md5sum -c "$EVIDENCE_DIR/evidence_md5.txt"

echo
echo "===== SHA256 VERIFICATION ====="
sha256sum -c "$EVIDENCE_DIR/evidence_sha256.txt"

echo
echo "Verification completed successfully."
