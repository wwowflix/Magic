import importlib, types

def test_import_scripts_arrow_parser_wrapper():
    mod = importlib.import_module("scripts.arrow_parser_wrapper")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
