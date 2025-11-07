import importlib, types


def test_import_scripts_phase00_INBOX__hypothesis_AF009BE2_AF009BE2():
    mod = importlib.import_module("scripts.phase00.INBOX._hypothesis_AF009BE2_AF009BE2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
