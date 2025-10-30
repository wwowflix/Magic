import importlib, types


def test_import_scripts_phase09_module_F_09F_redundant_script_paths_READY():
    mod = importlib.import_module(
        "scripts.phase09.module_F.09F_redundant_script_paths_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
