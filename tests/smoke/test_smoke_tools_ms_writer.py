import importlib
import types


def test_import_tools_ms_writer():
    mod = importlib.import_module("tools.ms_writer")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
