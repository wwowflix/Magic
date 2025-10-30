import importlib, types


def test_import_scripts_phase00_INBOX__oid_7B4796A3_7B4796A3():
    mod = importlib.import_module("scripts.phase00.INBOX._oid_7B4796A3_7B4796A3")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
