import importlib
import types


def test_import_scripts_phase18_module_C_18C_auto_create_notion_template_READY():
    mod = importlib.import_module(
        "scripts.phase18.module_C.18C_auto_create_notion_template_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
