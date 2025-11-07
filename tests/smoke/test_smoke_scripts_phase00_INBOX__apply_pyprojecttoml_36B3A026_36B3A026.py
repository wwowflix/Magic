import importlib, types


def test_import_scripts_phase00_INBOX__apply_pyprojecttoml_36B3A026_36B3A026():
    mod = importlib.import_module(
        "scripts.phase00.INBOX._apply_pyprojecttoml_36B3A026_36B3A026"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
