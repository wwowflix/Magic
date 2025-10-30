import importlib, types


def test_import_scripts_phase00_INBOX_editable_wheel_990B7FBD_990B7FBD():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.editable_wheel_990B7FBD_990B7FBD"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
