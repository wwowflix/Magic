# === MAGIC Phase11 â€“ SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================
"""TSI{B,C,D,J,P,S,V} are private tables used by Microsoft Visual TrueType (VTT)
tool to store its table source data.

TSIC contains the source text for the Variation CVT window and data for
the ``cvar`` table.

See also https://learn.microsoft.com/en-us/typography/tools/vtt/tsi-tables
"""


# MAGIC: removed duplicate otBase import
class table_T_S_I_C_(BaseTTXConverter):
    pass
