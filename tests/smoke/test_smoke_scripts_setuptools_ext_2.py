import importlib
import types


def test_import_scripts_setuptools_ext_2():
    mod = importlib.import_module("scripts.setuptools_ext_2")
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
