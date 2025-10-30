import importlib, types


def test_import_tools_generate_patch_csv():
    mod = importlib.import_module("tools.generate_patch_csv")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
