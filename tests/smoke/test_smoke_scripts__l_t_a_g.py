import importlib, types

def test_import_scripts__l_t_a_g():
    mod = importlib.import_module("scripts._l_t_a_g")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
