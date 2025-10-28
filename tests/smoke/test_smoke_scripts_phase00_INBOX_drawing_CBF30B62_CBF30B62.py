import importlib, types

def test_import_scripts_phase00_INBOX_drawing_CBF30B62_CBF30B62():
    mod = importlib.import_module("scripts.phase00.INBOX.drawing_CBF30B62_CBF30B62")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
