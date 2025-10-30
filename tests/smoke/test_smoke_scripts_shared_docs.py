import importlib, types


def test_import_scripts_shared_docs():
    mod = importlib.import_module("scripts.shared_docs")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
