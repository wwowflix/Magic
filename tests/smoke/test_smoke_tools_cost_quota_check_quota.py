import importlib, types


def test_import_tools_cost_quota_check_quota():
    mod = importlib.import_module("tools.cost_quota.check_quota")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
