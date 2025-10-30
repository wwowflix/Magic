import importlib, types


def test_import_scripts_phase00_INBOX_palette_9489EF47_9489EF47():
    mod = importlib.import_module("scripts.phase00.INBOX.palette_9489EF47_9489EF47")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
