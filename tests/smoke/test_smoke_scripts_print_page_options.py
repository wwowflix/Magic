import importlib, types

def test_import_scripts_print_page_options():
    mod = importlib.import_module("scripts.print_page_options")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
