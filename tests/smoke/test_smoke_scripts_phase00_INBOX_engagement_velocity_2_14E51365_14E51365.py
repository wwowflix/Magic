import importlib, types


def test_import_scripts_phase00_INBOX_engagement_velocity_2_14E51365_14E51365():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.engagement_velocity_2_14E51365_14E51365"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
