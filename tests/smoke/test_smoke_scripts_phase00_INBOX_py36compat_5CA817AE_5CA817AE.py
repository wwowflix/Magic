import importlib, types


def test_import_scripts_phase00_INBOX_py36compat_5CA817AE_5CA817AE():
    mod = importlib.import_module("scripts.phase00.INBOX.py36compat_5CA817AE_5CA817AE")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
