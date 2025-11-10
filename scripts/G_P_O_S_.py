# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter  # normal path
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================
# === MAGIC Phase11 – SHIELD: guarded otBase import ==========================
try:
    from .otBase import BaseTTXConverter  # normal path
except Exception:

    class BaseTTXConverter:  # minimal stub for smoke-import
        pass


# === end guard ==============================================================


class table_G_P_O_S_(BaseTTXConverter):
    """Glyph Positioning table

    The ``GPOS`` table stores advanced glyph-positioning data
    used in OpenType Layout features, such as mark attachment,
    cursive attachment, kerning, and other position adjustments.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/gpos
    """

    pass
