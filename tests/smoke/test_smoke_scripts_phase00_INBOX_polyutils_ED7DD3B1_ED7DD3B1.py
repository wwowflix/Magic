import importlib, types


def test_import_scripts_phase00_INBOX_polyutils_ED7DD3B1_ED7DD3B1():
    mod = importlib.import_module("scripts.phase00.INBOX.polyutils_ED7DD3B1_ED7DD3B1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
