import importlib, types


def test_import_scripts__g_l_y_f():
    mod = importlib.import_module("scripts._g_l_y_f")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
