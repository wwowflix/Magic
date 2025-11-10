import importlib
import types


def test_import_scripts_phase8_phase8_traffic_sentiment_analysis_READY():
    mod = importlib.import_module(
        "scripts.phase8.phase8_traffic_sentiment_analysis_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
