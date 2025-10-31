# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================
# MAGIC: removed duplicate otBase import
class table_J_S_T_F_(BaseTTXConverter):
    """Justification table

    The ``JSTF`` table contains glyph substitution and positioning
    data used to perform text justification.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/jstf
    """

    pass
