import importlib
import types


def test_import_scripts_web_audio():
    mod = importlib.import_module("scripts.web_audio")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
