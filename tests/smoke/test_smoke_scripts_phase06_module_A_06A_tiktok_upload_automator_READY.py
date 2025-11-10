import importlib, types


def test_import_scripts_phase06_module_A_06A_tiktok_upload_automator_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_A.06A_tiktok_upload_automator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
