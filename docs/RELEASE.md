# MAGIC Release Process — Week-2 Governance

## Branch Flow

main  release/vX.Y  prod-release

## Requirements to Merge into main

* CI must pass (Ruff + Pytest)
* CODEOWNERS review required
* Protected branch — no direct push allowed
* Signed commits recommended

## Tagging Process

git tag -a vX.Y.Z -m "release notes..."
git push origin vX.Y.Z

\# MAGIC Release Process



\## Branches

\- `main`: stable, protected

\- `prod-release`: production mirror (optional)



\## Versioning

\- Tags: `v<major>.<minor>.<patch>` (e.g. `v1.3.0`)

\- Special week tags: `week1-foundation-v1` (already created)



\## Standard release steps

1\. Create a release branch from `main`:

&nbsp;  - `git checkout main`

&nbsp;  - `git pull`

&nbsp;  - `git checkout -b release/v1.1.0`



2\. Run tests locally:

&nbsp;  - `pytest -q`

&nbsp;  - `pre-commit run --all-files`



3\. Open PR: `release/v1.1.0 -> main`

&nbsp;  - All required checks must pass.

&nbsp;  - Get at least 1 approval (you).



4\. Merge PR into `main`.



5\. Tag the release:

&nbsp;  - `git checkout main`

&nbsp;  - `git pull`

&nbsp;  - `git tag -a v1.1.0 -m "MAGIC v1.1.0 – summary"`

&nbsp;  - `git push origin v1.1.0`



6\. (Later, when Docker is ready) Push Docker image tagged `v1.1.0`.
