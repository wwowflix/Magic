def test_fonttools_has_featureparams_size():
    from fontTools.ttLib.tables import otTables as ot
    file_path = getattr(ot, "__file__", "?")
    assert hasattr(ot, "FeatureParamsSize"), (
        f"fontTools otTables missing FeatureParamsSize (otTables file={file_path})"
    )
