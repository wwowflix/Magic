# --- MAGIC Phase11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“ SHIELD: DistlibException shim ---
class DistlibException(Exception):
    """Minimal shim so resources and Scripts can import it during smoke."""

    pass


# --- end shim ---# === MAGIC Phase11 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“ SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================# MAGIC: removed duplicate otBase import
class table_V_V_A_R_(BaseTTXConverter):
    """Vertical Metrics Variations table

    The ``VVAR`` table contains variation data for per-glyph vertical metrics
    in a variable font.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/vvar
    """

    pass


# --- MAGIC shim: NBitBase for typing compat ---
if "NBitBase" not in globals():  # safe if NumPy-like typing provides it later

    class NBitBase:  # pragma: no cover
        __slots__ = ()

        def __repr__(self):  # minimal, never used at runtime
            return "NBitBase()"


try:
    __all__.append("NBitBase")
except Exception:
    try:
        __all__ = list(set((__all__ if "__all__" in globals() else []) + ["NBitBase"]))
    except Exception:
        pass
# --- end shim ---


# --- MAGIC fallback exports to avoid import-time breakage ---
def get_console(*a, **kw):
    return None
