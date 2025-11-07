import sys, importlib, inspect
from fontTools.ttLib import tables


def test_no_local_otTables_shadowing():
    """Ensure otTables is loaded from site-packages or builtin/frozen."""
    # Safe import
    try:
        ot = tables.otTables
    except AttributeError:
        from fontTools.ttLib.tables import otTables as ot

    # Try every way to locate path
    path = getattr(ot, "__file__", "")
    if not path:
        spec = getattr(ot, "__spec__", None)
        if spec and getattr(spec, "origin", None):
            path = spec.origin
    if not path:
        try:
            spec2 = importlib.util.find_spec("fontTools.ttLib.tables.otTables")
            if spec2 and getattr(spec2, "origin", None):
                path = spec2.origin
        except Exception:
            pass
    if not path:
        try:
            path = inspect.getfile(ot)
        except Exception:
            path = "(builtin or frozen)"

    print("Resolved otTables path:", path)
    assert any(
        kw in (path or "").lower() for kw in ("site-packages", "builtin", "frozen")
    ), f"otTables should come from site-packages or builtin/frozen module, got: {path}"
