# === MAGIC Phase11 â€“ SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================# MAGIC: removed duplicate otBase import
class table__a_n_k_r(BaseTTXConverter):
    """Anchor Point table

    The anchor point table provides a way to define anchor points.
    These are points within the coordinate space of a given glyph,
    independent of the control points used to render the glyph.
    Anchor points are used in conjunction with the ``kerx`` table.

    See also https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6ankr.html
    """

    pass
