import importlib, types


def test_import_scripts_phase00_INBOX_heap_profiler_AC2EEFFA_AC2EEFFA():
    mod = importlib.import_module(
        "scripts.phase00.INBOX.heap_profiler_AC2EEFFA_AC2EEFFA"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
