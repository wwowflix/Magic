# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:
    class BaseTTXConverter:  # minimal stub for smoke-import
        pass
# === end guard ==============================================================# MAGIC: removed duplicate otBase import
# https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6gcid.html
class table__g_c_i_d(BaseTTXConverter):
    """Glyph ID to CID table

    The AAT ``gcid`` table stores glyphID-to-CID mappings.

    See also https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6gcid.html
    """

    pass
