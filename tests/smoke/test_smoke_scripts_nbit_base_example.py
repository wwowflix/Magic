import importlib, types

def test_import_scripts_nbit_base_example():
    mod = importlib.import_module("scripts.nbit_base_example")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
