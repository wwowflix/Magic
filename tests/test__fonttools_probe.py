import sys
import pathlib


def test_fonttools_probe():
    import fontTools
    import fontTools.ttLib.tables.otTables as ot

    print("PY:", sys.version)
    print("fontTools:", fontTools.__version__)
    print("otTables file:", pathlib.Path(ot.__file__).as_posix())
    print("Has FeatureParamsSize:", hasattr(ot, "FeatureParamsSize"))
    assert hasattr(ot, "FeatureParamsSize")
