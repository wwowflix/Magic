import importlib, types


def test_import_scripts_phase05_module_C_05C_dynamic_text_overlay_generator_READY():
    mod = importlib.import_module(
        "scripts.phase05.module_C.05C_dynamic_text_overlay_generator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
