import importlib, types


def test_import_scripts_phase10_module_F_10F_traffic_source_mixer_READY():
    mod = importlib.import_module(
        "scripts.phase10.module_F.10F_traffic_source_mixer_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
