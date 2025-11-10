import importlib, types


def test_import_scripts_phase00_INBOX_T_S_I_D__EADAEE28_EADAEE28():
    mod = importlib.import_module("scripts.phase00.INBOX.T_S_I_D__EADAEE28_EADAEE28")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
