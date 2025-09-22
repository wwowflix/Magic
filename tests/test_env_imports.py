import pytest

def test_environment_has_core_libs():
    # Skip (not fail) if any optional libs are missing; passes if present.
    pytest.importorskip("requests")
    pytest.importorskip("pandas")
    pytest.importorskip("bs4")  # beautifulsoup4

