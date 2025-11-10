import importlib, types


def test_import_scripts_phase00_INBOX__p_o_s_t_B95DB0D1_B95DB0D1():
    mod = importlib.import_module("scripts.phase00.INBOX._p_o_s_t_B95DB0D1_B95DB0D1")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
