import importlib, types


def test_import_scripts_phase08_module_G_08G_export_to_notion_workspace_READY():
    mod = importlib.import_module(
        "scripts.phase08.module_G.08G_export_to_notion_workspace_READY"
    )
    assert isinstance(mod, types.ModuleType)
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()  # best-effort, ignore return
        except TypeError:
            pass
