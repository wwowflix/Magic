import importlib
import types


def test_import_scripts_phase17_module_D_17D_policy_violation_auto_flagger_READY():
    mod = importlib.import_module(
        "scripts.phase17.module_D.17D_policy_violation_auto_flagger_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
