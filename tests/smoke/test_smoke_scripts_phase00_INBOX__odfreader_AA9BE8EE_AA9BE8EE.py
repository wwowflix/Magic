import importlib, types


def test_import_scripts_phase00_INBOX__odfreader_AA9BE8EE_AA9BE8EE():
    mod = importlib.import_module("scripts.phase00.INBOX._odfreader_AA9BE8EE_AA9BE8EE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
