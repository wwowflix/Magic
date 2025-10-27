import importlib, types

def test_import_scripts_phase00_INBOX__highlevel_generic_6EDD5667_6EDD5667():
    mod = importlib.import_module("scripts.phase00.INBOX._highlevel_generic_6EDD5667_6EDD5667")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
