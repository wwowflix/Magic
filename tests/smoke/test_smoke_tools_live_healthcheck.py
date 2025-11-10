import importlib
import types


def test_import_tools_live_healthcheck():
    mod = importlib.import_module("tools.live_healthcheck")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
