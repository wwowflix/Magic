import importlib, types


def test_import_scripts_phase00_INBOX_builder_2_5E8A6969_5E8A6969():
    mod = importlib.import_module("scripts.phase00.INBOX.builder_2_5E8A6969_5E8A6969")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
