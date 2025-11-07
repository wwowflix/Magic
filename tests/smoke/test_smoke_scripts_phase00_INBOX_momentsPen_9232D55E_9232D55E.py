import importlib, types


def test_import_scripts_phase00_INBOX_momentsPen_9232D55E_9232D55E():
    mod = importlib.import_module("scripts.phase00.INBOX.momentsPen_9232D55E_9232D55E")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
