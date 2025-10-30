import importlib, types


def test_import_scripts_phase00_INBOX__resources_0EB62F90_0EB62F90():
    mod = importlib.import_module("scripts.phase00.INBOX._resources_0EB62F90_0EB62F90")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
