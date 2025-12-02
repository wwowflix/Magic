from __future__ import annotations

'''MAGIC Week 0 shim for scripts.enums.

Auto-generated placeholder to allow safe import during Week 0.
Real implementation will be added or restored in Week 1+.
'''

from typing import Any

__all__: list[str] = []


# ---------------------------------------------------------------------------
# MAGIC Week 0 shim: TextDirection (used by scripts.bidi)
# ---------------------------------------------------------------------------
try:
    from enum import Enum

    class TextDirection(Enum):
        LTR = "ltr"
        RTL = "rtl"
        TTB = "ttb"  # top-to-bottom
        BTT = "btt"  # bottom-to-top

except Exception:  # pragma: no cover
    TextDirection = object  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# MAGIC Week 0 shim: LanguageFilter (used by chardetect / prober chain)
# ---------------------------------------------------------------------------
from enum import IntEnum

class LanguageFilter(IntEnum):
    """
    Minimal Week 0 stand-in for charset detection language filtering.

    Real behaviour is not needed in Week 0 ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã¢â‚¬Â¦Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã¢â‚¬Å“ we only satisfy imports and
    basic comparisons.
    """
    NONE = 0
    CHINESE_SIMPLIFIED = 1
    CHINESE_TRADITIONAL = 2
    JAPANESE = 3
    KOREAN = 4

__all__ = globals().get("__all__", [])
for _name in ["LanguageFilter"]:
    if _name not in __all__:
        __all__.append(_name)

# ---------------------------------------------------------------------------
# MAGIC Week 0 shim: ProbingState (used by charsetprober / chardetect)
# ---------------------------------------------------------------------------
from enum import IntEnum

class ProbingState(IntEnum):
    """
    Minimal Week 0 stand-in for chardet ProbingState.

    We only care that members exist and comparisons like
    `state == ProbingState.FOUND_IT` work without crashing.
    """
    DETECTING = 0
    FOUND_IT = 1
    NOT_ME = 2

__all__ = globals().get("__all__", [])
for _name in ["ProbingState"]:
    if _name not in __all__:
        __all__.append(_name)

# ---------------------------------------------------------------------------
# MAGIC Week 0 shim: InputState (used by chardetect / universaldetector)
# ---------------------------------------------------------------------------
from enum import IntEnum

class InputState(IntEnum):
    """
    Minimal Week 0 stand-in for chardet InputState.

    We only need symbolic constants so the detector logic can compare
    states without failing import.
    """
    PURE_ASCII = 0
    ESC_ASCII = 1
    HIGH_BYTE = 2

__all__ = globals().get("__all__", [])
for _name in ["InputState"]:
    if _name not in __all__:
        __all__.append(_name)

# ---------------------------------------------------------------------------
# MAGIC Week 0 shim: MachineState (used by codingstatemachine / escprober)
# ---------------------------------------------------------------------------
from enum import IntEnum

class MachineState(IntEnum):
    """
    Minimal Week 0 stand-in for chardet MachineState.

    We just need symbolic constants so the state machine logic
    can compare states without failing import.
    """
    START = 0
    ERROR = 1
    ITS_ME = 2

__all__ = globals().get("__all__", [])
for _name in ["MachineState"]:
    if _name not in __all__:
        __all__.append(_name)

# ---------------------------------------------------------------------------
# MAGIC Week 0 shim: CharacterCategory / SequenceLikelihood
# (used by sbcharsetprober / chardetect charset detectors)
# ---------------------------------------------------------------------------
from enum import IntEnum

class CharacterCategory(IntEnum):
    """
    Minimal Week 0 stand-in for chardet CharacterCategory.

    Values are arbitrary but stable; they are only used symbolically
    in Week 0 so imports succeed.
    """
    UNDEFINED = 0
    CONTROL   = 1
    WHITESPACE = 2
    SYMBOL    = 3
    DIGIT     = 4
    LETTER    = 5

class SequenceLikelihood(IntEnum):
    """
    Minimal Week 0 stand-in for chardet SequenceLikelihood.
    """
    NEGATIVE = 0
    UNLIKELY = 1
    LIKELY   = 2
    POSITIVE = 3

__all__ = globals().get("__all__", [])
for _name in ["CharacterCategory", "SequenceLikelihood"]:
    if _name not in __all__:
        __all__.append(_name)

# ---------------------------------------------------------------------------
# MAGIC Week 0 final LanguageFilter override
# Ensures LanguageFilter.ALL exists for chardetect / universaldetector.
# ---------------------------------------------------------------------------
try:
    from enum import Enum

    class LanguageFilter(Enum):
        ALL = "all"
        CHINESE_SIMPLIFIED = "chs"
        CHINESE_TRADITIONAL = "cht"
        MINIMAL = "minimal"

except Exception:  # pragma: no cover
    LanguageFilter = object  # type: ignore[assignment]

__all__ = globals().get("__all__", [])
for _name in ["LanguageFilter"]:
    if _name not in __all__:
        __all__.append(_name)

# ---------------------------------------------------------------------------
# MAGIC Week 0 LanguageFilter override v2
# Ensures LanguageFilter has NONE / ALL / CHS / CHT / MINIMAL for chardet.
# ---------------------------------------------------------------------------
try:
    from enum import Enum

    class LanguageFilter(Enum):
        NONE = "none"
        ALL = "all"
        CHINESE_SIMPLIFIED = "chs"
        CHINESE_TRADITIONAL = "cht"
        MINIMAL = "minimal"

except Exception:  # pragma: no cover
    LanguageFilter = object  # type: ignore[assignment]

__all__ = globals().get("__all__", [])
for _name in ["LanguageFilter"]:
    if _name not in __all__:
        __all__.append(_name)

# ---------------------------------------------------------------------------
# MAGIC Week 0 shim: BlendMode (used by drawing / CSS rendering helpers)
# ---------------------------------------------------------------------------
try:
    from enum import Enum

    class BlendMode(Enum):
        NORMAL = "normal"
        MULTIPLY = "multiply"
        SCREEN = "screen"
        OVERLAY = "overlay"
        DARKEN = "darken"
        LIGHTEN = "lighten"

except Exception:  # pragma: no cover
    BlendMode = object  # type: ignore[assignment]

__all__ = globals().get("__all__", [])
for _name in ["BlendMode"]:
    if _name not in __all__:
        __all__.append(_name)
