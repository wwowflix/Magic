import importlib, types


def test_import_scripts_phase00_INBOX_image_D3B32E10_D3B32E10():
    mod = importlib.import_module("scripts.phase00.INBOX.image_D3B32E10_D3B32E10")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
