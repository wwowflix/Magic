$ErrorActionPreference = "Stop"

python -m pip install -U pip
python -m pip install -r requirements-dev.txt

$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
pytest -q tests/smoke/test_phase11A_ok.py -x
