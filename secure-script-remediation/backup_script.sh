#!/bin/bash

backup_dir=/tmp/backups
source_dir=$1

mkdir $backup_dir
cp -r $source_dir $backup_dir

timestamp=$(date +%Y%m%d)

mv $backup_dir/$(basename $source_dir) $backup_dir/backup_$timestamp

echo "Backup complete. Password: backup123" > $backup_dir/backup.log

echo "Backup completed"
