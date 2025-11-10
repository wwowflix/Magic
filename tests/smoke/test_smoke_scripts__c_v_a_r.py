import importlib, types


def test_import_scripts__c_v_a_r():
    mod = importlib.import_module("scripts._c_v_a_r")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
