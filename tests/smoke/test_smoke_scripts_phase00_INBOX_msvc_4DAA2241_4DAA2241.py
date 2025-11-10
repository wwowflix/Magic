import importlib, types


def test_import_scripts_phase00_INBOX_msvc_4DAA2241_4DAA2241():
    mod = importlib.import_module("scripts.phase00.INBOX.msvc_4DAA2241_4DAA2241")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
