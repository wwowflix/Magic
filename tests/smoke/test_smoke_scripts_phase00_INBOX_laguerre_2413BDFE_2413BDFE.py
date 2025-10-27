import importlib, types

def test_import_scripts_phase00_INBOX_laguerre_2413BDFE_2413BDFE():
    mod = importlib.import_module("scripts.phase00.INBOX.laguerre_2413BDFE_2413BDFE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
