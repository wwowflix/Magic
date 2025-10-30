import importlib, types


def test_import_scripts_phase00_INBOX__l_c_a_r_F16EB114_F16EB114():
    mod = importlib.import_module("scripts.phase00.INBOX._l_c_a_r_F16EB114_F16EB114")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
