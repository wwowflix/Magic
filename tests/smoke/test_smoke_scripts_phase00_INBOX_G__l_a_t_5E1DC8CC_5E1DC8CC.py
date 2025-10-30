import importlib, types


def test_import_scripts_phase00_INBOX_G__l_a_t_5E1DC8CC_5E1DC8CC():
    mod = importlib.import_module("scripts.phase00.INBOX.G__l_a_t_5E1DC8CC_5E1DC8CC")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
