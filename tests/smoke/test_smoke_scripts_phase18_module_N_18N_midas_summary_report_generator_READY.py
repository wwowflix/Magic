import importlib
import types


def test_import_scripts_phase18_module_N_18N_midas_summary_report_generator_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_N.18N_midas_summary_report_generator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
