import importlib, types


def test_import_scripts_phase00_INBOX_t2CharStringPen_1A01A495_1A01A495():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.t2CharStringPen_1A01A495_1A01A495"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
