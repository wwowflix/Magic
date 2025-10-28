import importlib, types

def test_import_tools_self_heal_agents():
    mod = importlib.import_module("tools.self_heal_agents")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
