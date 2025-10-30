import importlib, types


def test_import_scripts_phase03_module_A_03A_tiktok_hook_script_generator_READY():
    mod = importlib.import_module(
        "scripts.phase03.module_A.03A_tiktok_hook_script_generator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
