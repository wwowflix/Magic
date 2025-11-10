import importlib, types


def test_import_scripts__o_p_b_d():
    mod = importlib.import_module("scripts._o_p_b_d")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
