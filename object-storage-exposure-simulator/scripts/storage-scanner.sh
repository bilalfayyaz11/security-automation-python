#!/bin/bash

echo "==================================="
echo "Storage Exposure Detection Scanner"
echo "==================================="
echo ""

MINIO_HOST="http://localhost:9000"
BUCKETS=("private-bucket" "public-bucket" "exposed-data")

for bucket in "${BUCKETS[@]}"; do
    echo "Scanning bucket: $bucket"

    mc ls "localminio/$bucket/" 2>/dev/null | while read -r line; do
        filename=$(echo "$line" | awk '{print $NF}')

        if [ -n "$filename" ]; then
            file_response=$(curl -s -o /dev/null -w "%{http_code}" "$MINIO_HOST/$bucket/$filename")

            if [ "$file_response" = "200" ]; then
                echo "  [EXPOSED] $filename is publicly accessible"
            elif [ "$file_response" = "403" ]; then
                echo "  [SECURE] $filename is protected"
            else
                echo "  [UNKNOWN] $filename returned HTTP $file_response"
            fi
        fi
    done

    echo ""
done

echo "==================================="
echo "Scan Complete"
echo "==================================="
