import importlib, types


def test_import_scripts_phase00_INBOX_annotations_5C0F5306_5C0F5306():
    mod = importlib.import_module("scripts.phase00.INBOX.annotations_5C0F5306_5C0F5306")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
