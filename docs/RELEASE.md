# MAGIC Release Process — Week-2 Governance

## Branch Flow
main  release/vX.Y  prod-release

## Requirements to Merge into main
- CI must pass (Ruff + Pytest)
- CODEOWNERS review required
- Protected branch — no direct push allowed
- Signed commits recommended

## Tagging Process
git tag -a vX.Y.Z -m "release notes..."
git push origin vX.Y.Z
