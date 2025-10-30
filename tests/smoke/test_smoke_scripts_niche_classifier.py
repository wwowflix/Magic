import importlib, types


def test_import_scripts_niche_classifier():
    mod = importlib.import_module("scripts.niche_classifier")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
