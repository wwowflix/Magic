import sys
import pathlib
import importlib.util
import pytest

# Make repo root importable (for tools/* etc.)
ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Map test files to optional modules they require.
NEEDS = {
    # Week 8 dashboard test relies on pandas (and maybe matplotlib later)
    "tests/test_build_dashboard.py": "pandas",
    # Keep earlier skips you used on feature branches, harmless if files absent:
    "tests/test_create_manifest_covfill.py": "tools.create_manifest",
    "tests/test_remediator_unit.py": "tools.remediator",
}


def pytest_collection_modifyitems(config, items):
    skip_missing = pytest.mark.skip(reason="optional dependency missing in CI")
    for item in items:
        node = item.nodeid.split("::", 1)[0]
        mod = NEEDS.get(node)
        if mod and importlib.util.find_spec(mod) is None:
            item.add_marker(skip_missing)
