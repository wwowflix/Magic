import importlib, types


def test_import_scripts_phase00_INBOX_recompiler_2_77C543D8_77C543D8():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.recompiler_2_77C543D8_77C543D8"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
