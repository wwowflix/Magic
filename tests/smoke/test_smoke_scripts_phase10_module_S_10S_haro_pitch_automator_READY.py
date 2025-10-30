import importlib, types


def test_import_scripts_phase10_module_S_10S_haro_pitch_automator_READY():
    mod = importlib.import_module(
        "scripts.phase10.module_S.10S_haro_pitch_automator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
