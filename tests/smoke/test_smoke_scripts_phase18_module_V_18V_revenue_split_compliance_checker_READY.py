import importlib
import types


def test_import_scripts_phase18_module_V_18V_revenue_split_compliance_checker_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_V.18V_revenue_split_compliance_checker_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
