import importlib, types


def test_import_scripts_phase14_module_D_14D_channel_goal_alignment_engine_READY():
    mod = importlib.import_module(
        "scripts.phase14.module_D.14D_channel_goal_alignment_engine_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
