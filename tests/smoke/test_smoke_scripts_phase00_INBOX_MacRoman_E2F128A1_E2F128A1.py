import importlib, types


def test_import_scripts_phase00_INBOX_MacRoman_E2F128A1_E2F128A1():
    mod = importlib.import_module("scripts.phase00.INBOX.MacRoman_E2F128A1_E2F128A1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
