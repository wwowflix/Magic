import importlib, types


def test_import_scripts_phase13_module_H_13H_auto_link_rotation_engine_READY():
    mod = importlib.import_module(
        "scripts.phase13.module_H.13H_auto_link_rotation_engine_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
