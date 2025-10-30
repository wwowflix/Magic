import importlib
import sys, os

# Ensure site-packages appears before project root
site = os.path.join(sys.prefix, "Lib", "site-packages")
if site not in sys.path:
    sys.path.insert(0, site)


def test_import_scripts_BitmapGlyphMetrics():
    """Ensure BitmapGlyphMetrics imports correctly from real fontTools."""
    mod = importlib.import_module("scripts.BitmapGlyphMetrics")
    assert hasattr(mod, "__file__"), "Module did not load correctly"
    print("Loaded:", mod.__file__)
