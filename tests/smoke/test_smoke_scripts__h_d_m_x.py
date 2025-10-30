import importlib, types


def test_import_scripts__h_d_m_x():
    mod = importlib.import_module("scripts._h_d_m_x")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
