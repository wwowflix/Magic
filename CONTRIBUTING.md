# Contributing

All PRs to `main` must pass:
- `mypy` (type check)
- `tests` (pytest)

Quick start:

```bash
python -m pip install -U pip
pip install -r requirements.txt
pip install mypy pytest pytest-cov
mypy . --config-file mypy.ini
pytest -q
