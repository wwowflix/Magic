import importlib, types


def test_import_scripts_phase00_INBOX__m_a_x_p_7080C865_7080C865():
    mod = importlib.import_module("scripts.phase00.INBOX._m_a_x_p_7080C865_7080C865")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
