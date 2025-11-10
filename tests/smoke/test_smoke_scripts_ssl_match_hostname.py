import importlib
import types


def test_import_scripts_ssl_match_hostname():
    mod = importlib.import_module("scripts.ssl_match_hostname")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
