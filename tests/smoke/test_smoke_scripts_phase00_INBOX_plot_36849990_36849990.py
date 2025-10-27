import importlib, types

def test_import_scripts_phase00_INBOX_plot_36849990_36849990():
    mod = importlib.import_module("scripts.phase00.INBOX.plot_36849990_36849990")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
