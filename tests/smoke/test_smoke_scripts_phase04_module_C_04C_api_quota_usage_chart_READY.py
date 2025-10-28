import importlib, types

def test_import_scripts_phase04_module_C_04C_api_quota_usage_chart_READY():
    mod = importlib.import_module("scripts.phase04.module_C.04C_api_quota_usage_chart_READY")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
