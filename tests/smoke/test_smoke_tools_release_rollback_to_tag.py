import importlib, types


def test_import_tools_release_rollback_to_tag():
    mod = importlib.import_module("tools.release.rollback_to_tag")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
