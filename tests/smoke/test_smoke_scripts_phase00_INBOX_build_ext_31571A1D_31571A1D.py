import importlib, types


def test_import_scripts_phase00_INBOX_build_ext_31571A1D_31571A1D():
    mod = importlib.import_module("scripts.phase00.INBOX.build_ext_31571A1D_31571A1D")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
