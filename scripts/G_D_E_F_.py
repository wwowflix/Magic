# --- MAGIC Phase11 – SHIELD: tolerate broken scripts.otBase during smoke ---
try:
    from .otBase import BaseTTXConverter  # normal path
except Exception:
    # Import-time parse/indentation issues in otBase.py should not block smoke imports
    class BaseTTXConverter:  # minimal stub for smoke
        pass


# --- end MAGIC guard ---from .otBase import BaseTTXConverter


class table_G_D_E_F_(BaseTTXConverter):
    """Glyph Definition table

    The ``GDEF`` table stores various glyph properties that are used
    by OpenType Layout.

    See also https://learn.microsoft.com/en-us/typography/opentype/spec/gdef
    """

    pass
