import importlib, types

def test_import_scripts_G__l_o_c():
    mod = importlib.import_module("scripts.G__l_o_c")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
