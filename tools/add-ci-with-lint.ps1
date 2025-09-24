# tools/add-ci-with-lint.ps1
# Write/update CI with lint + tests + mypy, commit, and push the working branch.

$ErrorActionPreference = "Stop"

# Detect owner/repo from origin
$origin = git remote get-url origin
if ($origin -match '^https://github\.com/([^/]+)/([^\.]+)(?:\.git)?$') {
  $Owner,$Repo = $Matches[1],$Matches[2]
} elseif ($origin -match '^git@github\.com:([^/]+)/([^\.]+)(?:\.git)?$') {
  $Owner,$Repo = $Matches[1],$Matches[2]
} else { throw "Couldn't parse 'origin' remote ($origin)" }

# Current branch
$Branch = (git rev-parse --abbrev-ref HEAD).Trim()

New-Item -Type Directory -Force ".github/workflows" | Out-Null

$ci = @"
name: CI
on:
  push:
    branches: [ main, $Branch ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    name: lint
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install ruff
      - run: ruff check .

  tests:
    name: tests
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest -q

  mypy:
    name: mypy
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pip install mypy
      - run: mypy --install-types --non-interactive .
"@

$path = ".github/workflows/ci.yml"
$ci | Set-Content $path -Encoding UTF8

git add $path
git commit -m "ci: add/update lint job in CI workflow" 2>$null
git push origin $Branch

$actionsUrl = "https://github.com/$Owner/$Repo/actions?query=branch:$Branch"
Write-Host "✅ CI workflow updated and pushed to $Branch" -ForegroundColor Green
Write-Host "🔎 Watch the run: $actionsUrl" -ForegroundColor Cyan
Start-Process $actionsUrl
