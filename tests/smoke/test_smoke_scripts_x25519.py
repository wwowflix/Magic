import importlib, types


def test_import_scripts_x25519():
    mod = importlib.import_module("scripts.x25519")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
