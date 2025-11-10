import importlib, types


def test_import_scripts_phase10_module_B_10B_evergreen_vs_trending_split_READY():
    mod = importlib.import_module(
        "scripts.phase10.module_B.10B_evergreen_vs_trending_split_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
