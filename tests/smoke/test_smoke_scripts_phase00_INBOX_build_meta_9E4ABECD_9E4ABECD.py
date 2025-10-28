import importlib, types

def test_import_scripts_phase00_INBOX_build_meta_9E4ABECD_9E4ABECD():
    mod = importlib.import_module("scripts.phase00.INBOX.build_meta_9E4ABECD_9E4ABECD")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
