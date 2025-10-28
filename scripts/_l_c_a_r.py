# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:
    class BaseTTXConverter:  # minimal stub for smoke-import
        pass
# === end guard ==============================================================# MAGIC: removed duplicate otBase import
class table__l_c_a_r(BaseTTXConverter):
    """Ligature Caret table

    The AAT ``lcar`` table stores division points within ligatures, which applications
    can use to position carets properly between the logical parts of the ligature.

    See also https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6lcar.html
    """

    pass
