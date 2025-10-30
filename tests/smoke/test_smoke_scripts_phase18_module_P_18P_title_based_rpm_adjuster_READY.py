import importlib, types


def test_import_scripts_phase18_module_P_18P_title_based_rpm_adjuster_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_P.18P_title_based_rpm_adjuster_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
