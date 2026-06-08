#!/bin/bash

MOUNT_POINT="/mnt/evidence_vault"

if ! mount | grep -q "$MOUNT_POINT"; then
echo "Vault is not mounted"
exit 1
fi

cd "$MOUNT_POINT"

echo "Verifying evidence integrity..."

sudo sha256sum -c evidence_checksums.sha256

if [ $? -eq 0 ]; then
echo "All evidence files verified successfully"
else
echo "WARNING: Evidence integrity check FAILED"
fi
