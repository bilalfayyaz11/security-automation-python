#!/bin/bash

MOUNT_POINT="/mnt/evidence_vault"

if ! mountpoint -q "$MOUNT_POINT"; then
    echo "Error: Vault not mounted"
    exit 1
fi

echo "Verifying evidence integrity..."
cd "$MOUNT_POINT"
sudo sha256sum -c evidence_checksums.sha256

if [ $? -eq 0 ]; then
    echo "All evidence files verified successfully"
else
    echo "WARNING: Evidence integrity check FAILED"
fi
