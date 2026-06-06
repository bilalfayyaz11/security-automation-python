#!/bin/bash

set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <source_directory>"
    exit 1
fi

readonly BACKUP_DIR="/tmp/backups"
readonly SOURCE_DIR="$1"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist"
    exit 1
fi

mkdir -p "$BACKUP_DIR"

cp -r "$SOURCE_DIR" "$BACKUP_DIR"

timestamp=$(date +%Y%m%d)

source_basename=$(basename "$SOURCE_DIR")

mv "$BACKUP_DIR/$source_basename" "$BACKUP_DIR/backup_$timestamp"

echo "Backup completed at $(date)" >> "$BACKUP_DIR/backup.log"
echo "Backup location: $BACKUP_DIR/backup_$timestamp"

echo "Backup completed successfully"
