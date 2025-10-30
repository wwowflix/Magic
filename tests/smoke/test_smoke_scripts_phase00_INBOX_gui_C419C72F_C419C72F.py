import importlib, types


def test_import_scripts_phase00_INBOX_gui_C419C72F_C419C72F():
    mod = importlib.import_module("scripts.phase00.INBOX.gui_C419C72F_C419C72F")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
