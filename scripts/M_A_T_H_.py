# === MAGIC Phase11 â€“ SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================
class table_M_A_T_H_(BaseTTXConverter):
    """Mathematical Typesetting table

    The ``MATH`` table contains a variety of information needed to
    typeset glyphs in mathematical formulas and expressions.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/math
    """

    pass
