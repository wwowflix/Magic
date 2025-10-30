import importlib, types


def test_import_scripts_phase00_INBOX_ccompiler_A709E40F_A709E40F():
    mod = importlib.import_module("scripts.phase00.INBOX.ccompiler_A709E40F_A709E40F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
