#!/bin/bash
set -euo pipefail

echo "=== Starting Build Process ==="

BUILD_TIME=$(date '+%Y-%m-%d %H:%M:%S')
BUILD_DIR="build/release-$(date +%Y%m%d-%H%M%S)"

echo "Build Time: $BUILD_TIME"

echo "Running tests..."
python3 tests/test_app.py

mkdir -p "$BUILD_DIR"

echo "Packaging application..."
cp src/app.py "$BUILD_DIR/"

cat > "$BUILD_DIR/build-info.txt" << BUILDEOF
Build Date: $BUILD_TIME
Git Commit: $(git rev-parse --short HEAD 2>/dev/null || echo "N/A")
Version: $(grep __version__ src/app.py | cut -d'"' -f2)
BUILDEOF

echo "Build completed: $BUILD_DIR"
echo "=== Build Process Complete ==="
