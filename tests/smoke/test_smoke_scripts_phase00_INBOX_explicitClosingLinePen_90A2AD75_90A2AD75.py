import importlib, types


def test_import_scripts_phase00_INBOX_explicitClosingLinePen_90A2AD75_90A2AD75():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.explicitClosingLinePen_90A2AD75_90A2AD75"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
