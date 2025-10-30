import importlib, types


def test_import_scripts_phase00_INBOX__cmp_2_C0F97917_C0F97917():
    mod = importlib.import_module("scripts.phase00.INBOX._cmp_2_C0F97917_C0F97917")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
