import importlib
from pathlib import Path

def test_import_11d():
    mod = importlib.import_module("scripts.phase11.module_d.11D_api_callchain_integrity_READY")
    assert hasattr(mod, "main")

def test_has_api_config():
    assert Path("config/api_targets.json").exists()