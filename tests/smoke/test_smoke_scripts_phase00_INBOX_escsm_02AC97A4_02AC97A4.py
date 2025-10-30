import importlib, types


def test_import_scripts_phase00_INBOX_escsm_02AC97A4_02AC97A4():
    mod = importlib.import_module("scripts.phase00.INBOX.escsm_02AC97A4_02AC97A4")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
