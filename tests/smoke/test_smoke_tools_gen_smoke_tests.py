import importlib
import types


def test_import_tools_gen_smoke_tests():
    mod = importlib.import_module("tools.gen_smoke_tests")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
