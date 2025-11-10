import importlib
import types


def test_import_tools_ops_check_slo():
    mod = importlib.import_module("tools.ops.check_slo")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
