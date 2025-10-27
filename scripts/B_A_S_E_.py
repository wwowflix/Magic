# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter
except Exception:
    class BaseTTXConverter:  # minimal stub for smoke-import
        pass
# === end guard ==============================================================# MAGIC: removed duplicate otBase import
class table_B_A_S_E_(BaseTTXConverter):
    """Baseline table

    The ``BASE`` table contains information needed to align glyphs in
    different scripts, from different fonts, or at different sizes
    within the same line of text.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/base
    """

    pass
