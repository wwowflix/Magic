import importlib, types

def test_import_scripts_phase00_INBOX_bdist_rpm_87006847_87006847():
    mod = importlib.import_module("scripts.phase00.INBOX.bdist_rpm_87006847_87006847")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
