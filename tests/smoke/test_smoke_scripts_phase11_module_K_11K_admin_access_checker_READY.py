import importlib, types


def test_import_scripts_phase11_module_K_11K_admin_access_checker_READY():
    mod = importlib.import_module(
        "scripts.phase11.module_K.11K_admin_access_checker_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
