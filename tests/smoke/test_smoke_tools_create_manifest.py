import importlib, types


def test_import_tools_create_manifest():
    mod = importlib.import_module("tools.create_manifest")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
