#!/bin/bash
set -euo pipefail

VERSION=${1:-$(./scripts/version.sh get)}
PREVIOUS_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
OUTPUT_FILE="RELEASE_NOTES_${VERSION}.md"

echo "Generating release notes for version $VERSION..."

cat > "$OUTPUT_FILE" << HEADER
# Release Notes - Version $VERSION

**Release Date:** $(date '+%Y-%m-%d')

## Changes

HEADER

if [ -n "$PREVIOUS_TAG" ]; then
  {
    echo "Changes since $PREVIOUS_TAG:"
    echo ""
    echo "### Features"
  } >> "$OUTPUT_FILE"

  git log "$PREVIOUS_TAG"..HEAD --pretty=format:"- %s (%h)" --grep="^feat" >> "$OUTPUT_FILE" || true

  {
    echo ""
    echo ""
    echo "### Bug Fixes"
  } >> "$OUTPUT_FILE"

  git log "$PREVIOUS_TAG"..HEAD --pretty=format:"- %s (%h)" --grep="^fix" >> "$OUTPUT_FILE" || true

  {
    echo ""
    echo ""
    echo "### Other Changes"
  } >> "$OUTPUT_FILE"

  git log "$PREVIOUS_TAG"..HEAD --pretty=format:"- %s (%h)" --grep="^feat" --grep="^fix" --invert-grep >> "$OUTPUT_FILE" || true
else
  echo "Initial release - all commits:" >> "$OUTPUT_FILE"
  git log --pretty=format:"- %s (%h)" >> "$OUTPUT_FILE"
fi

{
  echo ""
  echo "---"
  echo "**Full Changelog:** Local repository history for v${VERSION}"
} >> "$OUTPUT_FILE"

echo "Release notes generated: $OUTPUT_FILE"
cat "$OUTPUT_FILE"
