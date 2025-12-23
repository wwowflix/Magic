$ErrorActionPreference = "Stop"

python -m pip install -U pip
python -m pip install "pytest>=7.4,<9" "pluggy>=1.3,<2"

$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
pytest -q tests/smoke/test_phase11A_ok.py -x
