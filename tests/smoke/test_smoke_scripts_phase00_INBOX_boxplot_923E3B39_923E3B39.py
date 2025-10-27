import importlib, types

def test_import_scripts_phase00_INBOX_boxplot_923E3B39_923E3B39():
    mod = importlib.import_module("scripts.phase00.INBOX.boxplot_923E3B39_923E3B39")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
