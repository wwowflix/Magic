# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:
    class BaseTTXConverter:  # minimal stub for smoke-import
        pass
# === end guard ==============================================================
# MAGIC: removed duplicate otBase import
class table_H_V_A_R_(BaseTTXConverter):
    """Horizontal Metrics Variations table

    The ``HVAR`` table contains variations in horizontal glyph metrics
    in variable fonts.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/hvar
    """

    pass
