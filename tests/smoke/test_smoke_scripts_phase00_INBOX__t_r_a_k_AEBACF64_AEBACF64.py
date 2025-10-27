import importlib, types

def test_import_scripts_phase00_INBOX__t_r_a_k_AEBACF64_AEBACF64():
    mod = importlib.import_module("scripts.phase00.INBOX._t_r_a_k_AEBACF64_AEBACF64")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
