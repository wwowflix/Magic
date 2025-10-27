import importlib, types

def test_import_scripts_S__i_l_f():
    mod = importlib.import_module("scripts.S__i_l_f")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
