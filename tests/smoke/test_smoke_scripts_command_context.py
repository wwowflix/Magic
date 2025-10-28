import importlib, types

def test_import_scripts_command_context():
    mod = importlib.import_module("scripts.command_context")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
