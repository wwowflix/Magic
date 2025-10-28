import importlib, types

def test_import_scripts_print_coercion_tables():
    mod = importlib.import_module("scripts.print_coercion_tables")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
