import importlib, types


def test_import_scripts_phase00_INBOX_x25519_FF89D079_FF89D079():
    mod = importlib.import_module("scripts.phase00.INBOX.x25519_FF89D079_FF89D079")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
