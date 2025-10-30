import importlib, types


def test_import_tools_patch_manifest_c():
    mod = importlib.import_module("tools.patch_manifest_c")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
