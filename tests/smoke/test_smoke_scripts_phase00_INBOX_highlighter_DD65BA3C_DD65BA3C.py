import importlib, types


def test_import_scripts_phase00_INBOX_highlighter_DD65BA3C_DD65BA3C():
    mod = importlib.import_module("scripts.phase00.INBOX.highlighter_DD65BA3C_DD65BA3C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
