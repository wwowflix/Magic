import importlib, types

def test_import_scripts_phase00_INBOX_build_clib_91D3EEAF_91D3EEAF():
    mod = importlib.import_module("scripts.phase00.INBOX.build_clib_91D3EEAF_91D3EEAF")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
