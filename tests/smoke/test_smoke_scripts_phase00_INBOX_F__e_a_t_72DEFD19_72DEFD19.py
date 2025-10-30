import importlib, types


def test_import_scripts_phase00_INBOX_F__e_a_t_72DEFD19_72DEFD19():
    mod = importlib.import_module("scripts.phase00.INBOX.F__e_a_t_72DEFD19_72DEFD19")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
