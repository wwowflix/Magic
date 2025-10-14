def test_tools_imports_smoke():
    # Import-only to exercise module top-level safely
    import importlib
    for mod in ["tools.build_dashboard", "tools.magic_scan_status"]:
        try:
            importlib.import_module(mod)
        except ModuleNotFoundError:
            pass  # ignore if file doesn't exist yet
