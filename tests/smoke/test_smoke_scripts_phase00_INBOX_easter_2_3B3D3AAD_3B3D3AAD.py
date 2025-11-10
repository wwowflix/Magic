import importlib, types


def test_import_scripts_phase00_INBOX_easter_2_3B3D3AAD_3B3D3AAD():
    mod = importlib.import_module("scripts.phase00.INBOX.easter_2_3B3D3AAD_3B3D3AAD")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
