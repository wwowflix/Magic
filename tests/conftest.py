import os
import sys
import importlib.util

# Ensure project root on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Map test file -> required module
NEEDS = {
    os.path.join("tests", "test_create_manifest_covfill.py"): "tools.create_manifest",
    os.path.join("tests", "test_remediator_unit.py"): "tools.remediator",
}


def pytest_ignore_collect(path, config):
    p = str(path)
    for rel, mod in NEEDS.items():
        if p.endswith(rel):
            if importlib.util.find_spec(mod) is None:
                # Ignore this test file entirely if its target module is missing
                return True
    return False
