# Releasing easyplots

## Quick Release

```bash
cd ~/src/hft-playground/hplot

# 1. Make your code changes, then bump version (e.g. 0.2.0 → 0.3.0)
sed -i '' 's/0.2.0/0.3.0/' pyproject.toml src/ezplot/__init__.py

# 2. Commit
git add .
git commit -m "v0.3.0: short description of changes"

# 3. Tag & push
git tag v0.3.0
git push && git push --tags
```

GitHub Actions will automatically build and publish to PyPI.

## Version Numbering

| Change type       | Example         | When to use                  |
|-------------------|-----------------|------------------------------|
| Patch `0.2.X`     | 0.2.0 → 0.2.1  | Bug fixes                    |
| Minor `0.X.0`     | 0.2.0 → 0.3.0  | New features, backward compatible |
| Major `X.0.0`     | 0.3.0 → 1.0.0  | Breaking changes             |

## Files to Update

1. `pyproject.toml` → `version = "X.Y.Z"`
2. `src/ezplot/__init__.py` → `__version__ = "X.Y.Z"`

Both must match the tag (without the `v` prefix).

## Verify

- GitHub Actions: https://github.com/ChaunceyDong/ezplot/actions
- PyPI: https://pypi.org/project/easyplots/
