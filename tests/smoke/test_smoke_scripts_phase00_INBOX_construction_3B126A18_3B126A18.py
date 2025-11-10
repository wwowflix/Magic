import importlib, types


def test_import_scripts_phase00_INBOX_construction_3B126A18_3B126A18():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.construction_3B126A18_3B126A18"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
