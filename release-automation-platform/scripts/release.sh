#!/bin/bash
set -euo pipefail

RELEASE_TYPE=${1:-patch}

echo "=== Starting Release Process ==="
echo "Release Type: $RELEASE_TYPE"

echo "Step 1: Bumping version..."
NEW_VERSION=$(./scripts/version.sh "$RELEASE_TYPE")
echo "New Version: $NEW_VERSION"

echo "Step 2: Running build..."
./scripts/build.sh

echo "Step 3: Committing version change..."
git add src/app.py
git commit -m "chore: bump version to $NEW_VERSION"

echo "Step 4: Creating git tag..."
if git rev-parse "v$NEW_VERSION" >/dev/null 2>&1; then
  git tag -d "v$NEW_VERSION"
fi
git tag -a "v$NEW_VERSION" -m "Release version $NEW_VERSION"

echo "Step 5: Generating release notes..."
./scripts/generate-release-notes.sh "$NEW_VERSION"

echo "Step 6: Creating release package..."
RELEASE_DIR="releases/v$NEW_VERSION"
LATEST_BUILD=$(ls -dt build/release-* | head -1)

mkdir -p "$RELEASE_DIR"
cp -r "$LATEST_BUILD"/* "$RELEASE_DIR/"
cp "RELEASE_NOTES_${NEW_VERSION}.md" "$RELEASE_DIR/"

echo ""
echo "=== Release Complete ==="
echo "Version: $NEW_VERSION"
echo "Tag: v$NEW_VERSION"
echo "Release Package: $RELEASE_DIR"
echo ""
echo "Next steps:"
echo "  - Review release notes: cat RELEASE_NOTES_${NEW_VERSION}.md"
echo "  - Push to remote: git push origin main --tags"
