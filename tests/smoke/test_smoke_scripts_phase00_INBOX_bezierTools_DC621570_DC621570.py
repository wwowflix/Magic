import importlib, types


def test_import_scripts_phase00_INBOX_bezierTools_DC621570_DC621570():
    mod = importlib.import_module("scripts.phase00.INBOX.bezierTools_DC621570_DC621570")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
