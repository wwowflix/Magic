import importlib
import types


def test_import_tools_publish_canary_post():
    mod = importlib.import_module("tools.publish.canary_post")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
