import importlib
import types


def test_import_scripts_phase18_module_A_18A_earnings_estimator_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_A.18A_earnings_estimator_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
