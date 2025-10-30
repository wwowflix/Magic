import importlib, types


def test_import_scripts_phase00_INBOX_py37compat_A496FFBE_A496FFBE():
    mod = importlib.import_module("scripts.phase00.INBOX.py37compat_A496FFBE_A496FFBE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
