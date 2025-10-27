import importlib, types

def test_import_scripts_phase00_INBOX__p_r_e_p_09C2ABE0_09C2ABE0():
    mod = importlib.import_module("scripts.phase00.INBOX._p_r_e_p_09C2ABE0_09C2ABE0")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
