#!/bin/bash

VAULT_IMAGE="$HOME/evidence-lab/evidence_vault.img"
VAULT_NAME="evidence_vault"
MOUNT_POINT="/mnt/evidence_vault"
KEY_FILE="$HOME/evidence-lab/vault.key"

case "$1" in
open)
sudo cryptsetup luksOpen "$VAULT_IMAGE" "$VAULT_NAME" \
--key-file "$KEY_FILE"

sudo mount /dev/mapper/"$VAULT_NAME" "$MOUNT_POINT"

echo "Vault opened and mounted"
;;

close)
sudo umount "$MOUNT_POINT" 2>/dev/null

sudo cryptsetup luksClose "$VAULT_NAME"

echo "Vault closed"
;;

status)
if mount | grep -q "$MOUNT_POINT"; then
echo "Vault OPEN"
else
echo "Vault CLOSED"
fi
;;

*)
echo "Usage: $0 {open|close|status}"
exit 1
;;
esac
