import importlib
import types


def test_import_tools_e2e_smoketest():
    mod = importlib.import_module("tools.e2e_smoketest")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
