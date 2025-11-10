import importlib, types


def test_import_scripts_phase00_INBOX__setmixin_5BDF9D9E_5BDF9D9E():
    mod = importlib.import_module("scripts.phase00.INBOX._setmixin_5BDF9D9E_5BDF9D9E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
