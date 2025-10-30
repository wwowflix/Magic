import importlib, types


def test_import_scripts_phase00_INBOX_f90mod_rules_DD422525_DD422525():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.f90mod_rules_DD422525_DD422525"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
