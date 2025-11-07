import importlib, types


def test_import_scripts__f_e_a_t():
    mod = importlib.import_module("scripts._f_e_a_t")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
