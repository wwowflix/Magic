import importlib, types


def test_import_scripts_phase00_INBOX_featureVars_2_A0FA9296_A0FA9296():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.featureVars_2_A0FA9296_A0FA9296"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
