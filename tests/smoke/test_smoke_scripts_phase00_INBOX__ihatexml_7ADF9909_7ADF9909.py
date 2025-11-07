import importlib, types


def test_import_scripts_phase00_INBOX__ihatexml_7ADF9909_7ADF9909():
    mod = importlib.import_module("scripts.phase00.INBOX._ihatexml_7ADF9909_7ADF9909")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
