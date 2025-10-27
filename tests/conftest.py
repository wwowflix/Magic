import os, sys, pathlib
# Put project root (the directory containing this conftest) on sys.path
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---- existing fixtures (keep any you already had) ----
import sqlite3
import pytest

@pytest.fixture
def tmp_db_path(tmp_path):
    db = tmp_path / "test.sqlite"
    return str(db)
