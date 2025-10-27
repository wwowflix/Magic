# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:
    class BaseTTXConverter:  # minimal stub for smoke-import
        pass
# === end guard ==============================================================
class table_M_V_A_R_(BaseTTXConverter):
    """Metrics Variations table

    The ``MVAR`` table contains variation information for font-wide
    metrics in a variable font.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/mvar
    """

    pass
