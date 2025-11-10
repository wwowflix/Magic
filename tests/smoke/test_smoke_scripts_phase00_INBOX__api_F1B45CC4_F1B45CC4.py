import importlib, types


def test_import_scripts_phase00_INBOX__api_F1B45CC4_F1B45CC4():
    mod = importlib.import_module("scripts.phase00.INBOX._api_F1B45CC4_F1B45CC4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
