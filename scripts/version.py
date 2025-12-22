import importlib.metadata

try:
    __version__ = importlib.metadata.version("snscrape")
except importlib.metadata.PackageNotFoundError:
    __version__ = None

# ======================================================================
# MAGIC Week 0 additions – distlib-style compatibility shims
# ======================================================================

class UnsupportedVersionError(Exception):
    """
    MAGIC shim for distlib.version.UnsupportedVersionError.

    In our Week 0 import tests we never expect this to be actually raised.
    """


def get_scheme(name: str = "default"):
    """
    MAGIC shim for distlib.version.get_scheme.

    The real function returns an object that knows how to compute version
    numbers, tags, etc.  For our purposes we just return a tiny object
    with a `tag` method so imports succeed.
    """

    class _DummyScheme:
        def tag(self, *args, **kwargs) -> str:
            return "0.0.0"

    return _DummyScheme()
