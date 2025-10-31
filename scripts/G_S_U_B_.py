# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================


# MAGIC: removed duplicate otBase import
class table_G_S_U_B_(BaseTTXConverter):
    """Glyph Substitution table

    The ``GSUB`` table contains glyph-substitution rules used in
    OpenType Layout.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/gsub
    """

    pass
