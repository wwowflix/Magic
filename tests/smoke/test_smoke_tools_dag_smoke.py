import importlib
import types


def test_import_tools_dag_smoke():
    mod = importlib.import_module("tools.dag_smoke")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
