import importlib, types

def test_import_tools_magic_phase11_full_cycle():
    mod = importlib.import_module("tools.magic_phase11_full_cycle")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
