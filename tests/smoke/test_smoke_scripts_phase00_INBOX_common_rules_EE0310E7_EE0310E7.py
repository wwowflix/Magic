import importlib, types


def test_import_scripts_phase00_INBOX_common_rules_EE0310E7_EE0310E7():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.common_rules_EE0310E7_EE0310E7"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
