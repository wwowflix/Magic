import importlib, types


def test_import_scripts_phase00_INBOX_rrule_2_DF791649_DF791649():
    mod = importlib.import_module("scripts.phase00.INBOX.rrule_2_DF791649_DF791649")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
