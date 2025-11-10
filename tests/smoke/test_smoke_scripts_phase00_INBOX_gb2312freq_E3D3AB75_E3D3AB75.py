import importlib, types


def test_import_scripts_phase00_INBOX_gb2312freq_E3D3AB75_E3D3AB75():
    mod = importlib.import_module("scripts.phase00.INBOX.gb2312freq_E3D3AB75_E3D3AB75")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
