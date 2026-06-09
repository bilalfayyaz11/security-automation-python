#!/bin/bash
set -euo pipefail

VERSION_FILE="src/app.py"

if [ ! -f "$VERSION_FILE" ]; then
  echo "Version file not found: $VERSION_FILE"
  exit 1
fi

CURRENT_VERSION=$(grep __version__ "$VERSION_FILE" | cut -d'"' -f2)

get_version() {
  echo "$CURRENT_VERSION"
}

bump_version() {
  local bump_type=$1
  IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"

  case "$bump_type" in
    major)
      major=$((major + 1))
      minor=0
      patch=0
      ;;
    minor)
      minor=$((minor + 1))
      patch=0
      ;;
    patch)
      patch=$((patch + 1))
      ;;
    *)
      echo "Usage: $0 {get|major|minor|patch}"
      exit 1
      ;;
  esac

  NEW_VERSION="$major.$minor.$patch"

  sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" "$VERSION_FILE"

  echo "$NEW_VERSION"
}

case "${1:-get}" in
  get)
    get_version
    ;;
  major|minor|patch)
    bump_version "$1"
    ;;
  *)
    echo "Usage: $0 {get|major|minor|patch}"
    exit 1
    ;;
esac
