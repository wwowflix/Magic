import importlib, types


def test_import_scripts_phase00_INBOX_usedoctest_2_B4F96657_B4F96657():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.usedoctest_2_B4F96657_B4F96657"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
