import importlib, types


def test_import_scripts_phase00_INBOX_types_2_D8AE13E6_D8AE13E6():
    mod = importlib.import_module("scripts.phase00.INBOX.types_2_D8AE13E6_D8AE13E6")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
