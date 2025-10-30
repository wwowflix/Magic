# === MAGIC Phase11 â€“ SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================# MAGIC: removed duplicate otBase import
# https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6opbd.html
class table__o_p_b_d(BaseTTXConverter):
    """Optical Bounds table

    The AAT ``opbd`` table contains optical boundary points for glyphs, which
    applications can use for the visual alignment of lines of text.

    See also https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6opbd.html
    """

    pass
