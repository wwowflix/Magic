import importlib, types

def test_import_scripts_phase06_module_Y_06Y_upload_to_cloud_backup_READY():
    mod = importlib.import_module("scripts.phase06.module_Y.06Y_upload_to_cloud_backup_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
