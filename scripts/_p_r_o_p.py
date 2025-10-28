# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:
    class BaseTTXConverter:  # minimal stub for smoke-import
        pass
# === end guard ==============================================================# MAGIC: removed duplicate otBase import
# https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6prop.html
class table__p_r_o_p(BaseTTXConverter):
    """The AAT ``prop`` table can store a variety of per-glyph properties, such as
       Unicode directionality or whether glyphs are non-spacing marks.

    See also https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6prop.html
    """

    pass
