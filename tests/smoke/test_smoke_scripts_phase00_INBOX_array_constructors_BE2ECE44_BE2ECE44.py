import importlib, types


def test_import_scripts_phase00_INBOX_array_constructors_BE2ECE44_BE2ECE44():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.array_constructors_BE2ECE44_BE2ECE44"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
