import importlib
import types


def test_import_tools_backup_manifest():
    mod = importlib.import_module("tools.backup_manifest")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
