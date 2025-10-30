import importlib, types


def test_import_scripts_phase00_INBOX__asarray_C706F58E_C706F58E():
    mod = importlib.import_module("scripts.phase00.INBOX._asarray_C706F58E_C706F58E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
