import importlib, pathlib
def test_import_11d():
    m = importlib.import_module("scripts.phase11.module_d.11D_api_callchain_verifier_READY")
    assert hasattr(m, "main")
def test_config_exists():
    assert pathlib.Path("config/api_chain_rules.json").exists()