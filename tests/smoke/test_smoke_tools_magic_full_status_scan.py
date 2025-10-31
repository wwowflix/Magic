import importlib
import types


def test_import_tools_magic_full_status_scan():
    mod = importlib.import_module("tools.magic_full_status_scan")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
