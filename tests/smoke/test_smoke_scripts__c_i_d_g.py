import importlib, types


def test_import_scripts__c_i_d_g():
    mod = importlib.import_module("scripts._c_i_d_g")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
