import importlib
import types


def test_import_scripts_phase18_module_Y_18Y_seasonal_trend_monetization_mapper_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_Y.18Y_seasonal_trend_monetization_mapper_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
