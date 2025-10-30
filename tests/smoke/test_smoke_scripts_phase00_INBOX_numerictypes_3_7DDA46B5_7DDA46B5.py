import importlib, types


def test_import_scripts_phase00_INBOX_numerictypes_3_7DDA46B5_7DDA46B5():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.numerictypes_3_7DDA46B5_7DDA46B5"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
