#!/bin/bash
# File Integrity Checker
# Generates and verifies SHA256 checksums for monitored files.

set -u

generate_checksums() {
    local directory="${1:-.}"
    local output_file="checksums.sha256"

    if [ ! -d "$directory" ]; then
        echo "Error: Directory not found: $directory"
        exit 1
    fi

    echo "Generating checksums for text files in $directory..."

    find "$directory" \
        -type f \
        -name "*.txt" \
        -not -name "$output_file" \
        -print0 | sort -z | xargs -0 sha256sum > "$output_file"

    echo "Checksums saved to $output_file"
}

verify_checksums() {
    local checksum_file="${1:-checksums.sha256}"

    if [ ! -f "$checksum_file" ]; then
        echo "Error: Checksum file not found: $checksum_file"
        exit 1
    fi

    echo "Verifying file integrity..."
    sha256sum -c "$checksum_file"
}

case "${1:-}" in
    generate)
        generate_checksums "${2:-.}"
        ;;
    verify)
        verify_checksums "${2:-checksums.sha256}"
        ;;
    *)
        echo "Usage: $0 {generate|verify} [path]"
        echo "Examples:"
        echo "  $0 generate ."
        echo "  $0 verify checksums.sha256"
        exit 1
        ;;
esac
