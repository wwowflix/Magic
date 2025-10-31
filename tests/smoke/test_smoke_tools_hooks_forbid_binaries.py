import importlib
import types


def test_import_tools_hooks_forbid_binaries():
    mod = importlib.import_module("tools.hooks.forbid_binaries")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
