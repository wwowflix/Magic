import importlib, types

def test_import_scripts_phase00_INBOX_setuptools_ext_2_3F03ED58_3F03ED58():
    mod = importlib.import_module("scripts.phase00.INBOX.setuptools_ext_2_3F03ED58_3F03ED58")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
