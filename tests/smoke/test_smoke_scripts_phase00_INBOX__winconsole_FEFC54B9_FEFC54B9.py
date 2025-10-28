import importlib, types

def test_import_scripts_phase00_INBOX__winconsole_FEFC54B9_FEFC54B9():
    mod = importlib.import_module("scripts.phase00.INBOX._winconsole_FEFC54B9_FEFC54B9")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
