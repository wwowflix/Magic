## PR Checklist
- [ ] Tests pass locally (`pytest -q`)
- [ ] Type checks pass (`mypy .`)
- [ ] Coverage ≥ 75% (`pytest --cov=./ --cov-fail-under=75`)
- [ ] Security scans clean (`pip-audit`, `safety`, `bandit`)
- [ ] No secrets leaked (`gitleaks` / `detect-secrets`)
- [ ] SBOM updated if deps changed (`cyclonedx-py`)
