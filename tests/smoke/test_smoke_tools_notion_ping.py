import importlib
import types


def test_import_tools_notion_ping():
    mod = importlib.import_module("tools.notion_ping")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
