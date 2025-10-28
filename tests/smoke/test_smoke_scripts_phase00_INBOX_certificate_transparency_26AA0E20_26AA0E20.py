import importlib, types

def test_import_scripts_phase00_INBOX_certificate_transparency_26AA0E20_26AA0E20():
    mod = importlib.import_module("scripts.phase00.INBOX.certificate_transparency_26AA0E20_26AA0E20")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
