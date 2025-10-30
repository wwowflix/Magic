# === MAGIC Phase11 â€“ SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================# MAGIC: removed duplicate otBase import
class table_V_A_R_C_(BaseTTXConverter):
    """Variable Components table

    The ``VARC`` table contains variation information for composite glyphs.

    See also https://github.com/harfbuzz/boring-expansion-spec/blob/main/VARC.md
    """

    pass
