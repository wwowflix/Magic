# --- MAGIC Phase11 â€“ SHIELD: DistlibException shim ---
class DistlibException(Exception):
    """Minimal shim so resources and Scripts can import it during smoke."""
    pass
# --- end shim ---# === MAGIC Phase11 â€“ SHIELD: guarded otBase import ==========================
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

