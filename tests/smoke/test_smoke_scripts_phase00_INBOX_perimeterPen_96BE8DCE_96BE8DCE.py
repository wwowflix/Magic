import importlib, types


def test_import_scripts_phase00_INBOX_perimeterPen_96BE8DCE_96BE8DCE():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.perimeterPen_96BE8DCE_96BE8DCE"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
