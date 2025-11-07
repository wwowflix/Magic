import importlib, types


def test_import_scripts_phase00_INBOX_escprober_2A1A38F1_2A1A38F1():
    mod = importlib.import_module("scripts.phase00.INBOX.escprober_2A1A38F1_2A1A38F1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
