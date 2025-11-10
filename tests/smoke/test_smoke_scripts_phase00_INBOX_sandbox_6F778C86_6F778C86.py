import importlib, types


def test_import_scripts_phase00_INBOX_sandbox_6F778C86_6F778C86():
    mod = importlib.import_module("scripts.phase00.INBOX.sandbox_6F778C86_6F778C86")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
