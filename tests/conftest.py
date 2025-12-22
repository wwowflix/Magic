import sys, types


def _ensure_mod(qualname: str):
    parts = qualname.split(".")
    parent = None
    path = []
    for p in parts:
        path.append(p)
        name = ".".join(path)
        if name not in sys.modules:
            m = types.ModuleType(name)
            sys.modules[name] = m
            if parent is not None:
                setattr(parent, p, m)
        parent = sys.modules[name]
    return sys.modules[qualname]


def _stub(name: str, attrs: dict | None = None):
    m = _ensure_mod(name)
    if attrs:
        for k, v in attrs.items():
            setattr(m, k, v)
    return m


# Light, import-only stubs for optional/expensive deps
for mod in [
    "cryptography",
    "selenium",
    "fsspec",
    "altair",
    "greenlet",
    "cmdstanpy",
    "tables",
    "TikTokApi",
    "websocket",
    "jinja2",
    "hypothesis",
]:
    _stub(mod)

# bs4 and bs4.element
_stub("bs4")
_stub("bs4.element")

# pip._vendor.chardet
_stub("pip")
_stub("pip._vendor")
_stub("pip._vendor.chardet")

# fontTools / fonttools with minimal otTables surface used by your vendors
_stub("fontTools")
_stub("fontTools.ttLib")
ot = _stub(
    "fontTools.ttLib.tables.otTables",
    {
        "FeatureParamsSize": type("FeatureParamsSize", (), {})(),
        "FeatureParamsStylisticSet": type("FeatureParamsStylisticSet", (), {})(),
        "STAT": type("STAT", (), {})(),
        "AxisRecord": type("AxisRecord", (), {})(),
        "AxisValue": type("AxisValue", (), {})(),
        "FeatureName": type("FeatureName", (), {})(),
        "Setting": type("Setting", (), {})(),
    },
)
# alias lowercase package name some libs use
sys.modules["fonttools"] = sys.modules["fontTools"]
# Add hypothesis minimal symbols used by pytest plugin
import sys

if "hypothesis" in sys.modules:
    sys.modules["hypothesis"].is_hypothesis_test = lambda obj=None: False
# Safety: if a stub 'hypothesis' exists, give it the attributes pytest plugin expects
import sys, types

if "hypothesis" not in sys.modules:
    m = types.ModuleType("hypothesis")
    sys.modules["hypothesis"] = m
if not hasattr(sys.modules["hypothesis"], "core"):
    sys.modules["hypothesis"].core = object()
if "hypothesis.internal" not in sys.modules:
    mi = types.ModuleType("hypothesis.internal")
    sys.modules["hypothesis.internal"] = mi
if "hypothesis.internal.observability" not in sys.modules:
    mo = types.ModuleType("hypothesis.internal.observability")
    sys.modules["hypothesis.internal.observability"] = mo
    mo._WROTE_TO = set()

import tests.auto_shims  # magic import shims

# ---- auto-added by MAGIC helper ----
import os, sqlite3
import pytest

@pytest.fixture
def tmp_db_path(tmp_path):
    """Return a temp SQLite database file path and ensure it exists.
    Also create a minimal 'trends' table if your collector expects it.
    """
    db = tmp_path / "trends.db"
    con = sqlite3.connect(db)
    try:
        con.execute("CREATE TABLE IF NOT EXISTS trends (id INTEGER PRIMARY KEY, ts TEXT, name TEXT, value REAL)")
        con.commit()
    finally:
        con.close()
    return str(db)

@pytest.fixture
def tmp_db_url(tmp_db_path):
    return f"sqlite:///{tmp_db_path}"

@pytest.fixture
def magic_test_env(monkeypatch, tmp_path, tmp_db_path):
    monkeypatch.setenv("MAGIC_DB_URL", f"sqlite:///{tmp_db_path}")
    monkeypatch.setenv("MAGIC_OUTPUTS_DIR", str(tmp_path))
    return tmp_path
# ---- end MAGIC helper ----
