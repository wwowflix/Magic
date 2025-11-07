import importlib, types


def test_import_scripts_phase10_module_J_10J_comment_sentiment_analyzer_READY():
    mod = importlib.import_module(
        "scripts.phase10.module_J.10J_comment_sentiment_analyzer_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
