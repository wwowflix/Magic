import importlib, types

def test_import_scripts_phase00_INBOX__manylinux_5DC6E25C_5DC6E25C():
    mod = importlib.import_module("scripts.phase00.INBOX._manylinux_5DC6E25C_5DC6E25C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
