#!/bin/bash

VAULT_IMAGE="$HOME/evidence-lab/evidence_vault.img"
VAULT_NAME="evidence_vault"
MOUNT_POINT="/mnt/evidence_vault"
KEY_FILE="$HOME/evidence-lab/vault.key"

case "$1" in
    open)
        echo "Opening evidence vault..."
        sudo cryptsetup luksOpen "$VAULT_IMAGE" "$VAULT_NAME" --key-file "$KEY_FILE"
        sudo mount /dev/mapper/"$VAULT_NAME" "$MOUNT_POINT"
        echo "Vault opened and mounted at $MOUNT_POINT"
        ;;
    close)
        echo "Closing evidence vault..."
        sudo umount "$MOUNT_POINT"
        sudo cryptsetup luksClose "$VAULT_NAME"
        echo "Vault closed securely"
        ;;
    status)
        if [ -e /dev/mapper/"$VAULT_NAME" ]; then
            echo "Vault is OPEN"
            df -h | grep "$VAULT_NAME"
        else
            echo "Vault is CLOSED"
        fi
        ;;
    *)
        echo "Usage: $0 {open|close|status}"
        exit 1
        ;;
esac
