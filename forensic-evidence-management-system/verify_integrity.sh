#!/bin/bash

set -e

echo "=== Evidence Integrity Verification ==="
echo

cd ~/forensics_lab/evidence/original

echo "Verifying SHA256 hashes..."
sha256sum -c ../hashes/sha256_manifest.txt

echo
echo "Verification complete."
echo

echo "Checking evidence protection..."
ls -l
