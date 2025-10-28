import importlib, types

def test_import_tools_emit_metrics_from_summaries():
    mod = importlib.import_module("tools.emit_metrics_from_summaries")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
