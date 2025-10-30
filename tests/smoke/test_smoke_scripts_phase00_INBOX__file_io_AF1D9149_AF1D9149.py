import importlib, types


def test_import_scripts_phase00_INBOX__file_io_AF1D9149_AF1D9149():
    mod = importlib.import_module("scripts.phase00.INBOX._file_io_AF1D9149_AF1D9149")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
