import importlib, types


def test_import_scripts_phase06_module_Q_06Q_auto_summary_of_each_post_READY():
    mod = importlib.import_module(
        "scripts.phase06.module_Q.06Q_auto_summary_of_each_post_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
