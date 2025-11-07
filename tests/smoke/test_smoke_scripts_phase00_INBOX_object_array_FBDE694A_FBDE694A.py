import importlib, types


def test_import_scripts_phase00_INBOX_object_array_FBDE694A_FBDE694A():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.object_array_FBDE694A_FBDE694A"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
