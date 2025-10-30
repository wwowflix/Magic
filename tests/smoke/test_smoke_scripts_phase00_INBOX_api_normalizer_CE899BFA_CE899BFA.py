import importlib, types


def test_import_scripts_phase00_INBOX_api_normalizer_CE899BFA_CE899BFA():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.api_normalizer_CE899BFA_CE899BFA"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
