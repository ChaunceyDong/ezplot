#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: ./release.sh <version> [message]"
    echo "  e.g. ./release.sh 0.2.1 'fix import bug'"
    exit 1
fi

VERSION="$1"
MSG="${2:-v$VERSION}"
CURRENT=$(grep -oP 'version = "\K[^"]+' pyproject.toml)

echo "Bumping version: $CURRENT -> $VERSION"

# 1. Bump version in both files
sed -i "s/version = \"$CURRENT\"/version = \"$VERSION\"/" pyproject.toml
sed -i "s/__version__ = \"$CURRENT\"/__version__ = \"$VERSION\"/" src/ezplot/__init__.py

# 2. Verify import
PYTHONPATH=src python -c "import ezplot; assert ezplot.__version__ == '$VERSION', f'Version mismatch: {ezplot.__version__}'"
echo "Import check passed"

# 3. Commit, tag, push
git add pyproject.toml src/ezplot/__init__.py
git commit -m "v$VERSION: $MSG"
git tag "v$VERSION"
git push && git push origin "v$VERSION"

echo "Released v$VERSION"
