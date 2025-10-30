import importlib, types


def test_import_scripts_phase00_INBOX__m_o_r_x_3B06A656_3B06A656():
    mod = importlib.import_module("scripts.phase00.INBOX._m_o_r_x_3B06A656_3B06A656")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
