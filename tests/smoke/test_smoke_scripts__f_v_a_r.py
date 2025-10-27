import importlib, types

def test_import_scripts__f_v_a_r():
    mod = importlib.import_module("scripts._f_v_a_r")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
