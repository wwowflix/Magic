import importlib, types


def test_import_scripts_phase08_module_G_08G_weekly_convertkit_email_sync_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_G.08G_weekly_convertkit_email_sync_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
