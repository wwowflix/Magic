import importlib, types


def test_import_scripts_data_user_prefs_data_user_prefs_placeholder_READY():
    mod = importlib.import_module(
        "scripts.data.user_prefs.data_user_prefs_placeholder_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
