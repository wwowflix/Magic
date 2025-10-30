import importlib, types


def test_import_scripts_phase00_INBOX__s_b_i_x_B6490A6C_B6490A6C():
    mod = importlib.import_module("scripts.phase00.INBOX._s_b_i_x_B6490A6C_B6490A6C")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
