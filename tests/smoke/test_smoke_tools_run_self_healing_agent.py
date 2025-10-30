import importlib, types


def test_import_tools_run_self_healing_agent():
    mod = importlib.import_module("tools.run_self_healing_agent")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
