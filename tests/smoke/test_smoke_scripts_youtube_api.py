import importlib
import types


def test_import_scripts_youtube_api():
    mod = importlib.import_module("scripts.youtube_api")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
