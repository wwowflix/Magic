import importlib, types


def test_import_scripts_phase00_INBOX_extending_2_5328E436_5328E436():
    mod = importlib.import_module("scripts.phase00.INBOX.extending_2_5328E436_5328E436")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
