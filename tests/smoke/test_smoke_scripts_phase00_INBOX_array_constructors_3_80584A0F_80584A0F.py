import importlib, types


def test_import_scripts_phase00_INBOX_array_constructors_3_80584A0F_80584A0F():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.array_constructors_3_80584A0F_80584A0F"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
