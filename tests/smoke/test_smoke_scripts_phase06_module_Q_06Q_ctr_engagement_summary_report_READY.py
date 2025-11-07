import importlib, types


def test_import_scripts_phase06_module_Q_06Q_ctr_engagement_summary_report_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_Q.06Q_ctr_engagement_summary_report_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
