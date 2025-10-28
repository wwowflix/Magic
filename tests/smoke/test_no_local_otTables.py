def test_no_local_otTables_shadowing():
    import sys
    from fontTools.ttLib.tables import otTables as ot
    # Ensure we resolved the library module, not something under scripts/
    path = getattr(ot, "__file__", "") or ""
    assert "site-packages" in path.lower(), f"otTables should come from site-packages, got: {path}"
