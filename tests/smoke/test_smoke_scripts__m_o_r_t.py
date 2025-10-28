import importlib, types

def test_import_scripts__m_o_r_t():
    mod = importlib.import_module("scripts._m_o_r_t")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
