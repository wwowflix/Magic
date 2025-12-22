"""
MAGIC stub for scripts.color

This module provides just enough of a Rich-style color interface for
other MAGIC shims to import:

    from .color import Color, ColorParseError, ColorSystem, blend_rgb

It is *not* a full colour management system; it only needs to satisfy
imports and simple helper usage in scripts.style / scripts._inspect.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Tuple, Union


class ColorParseError(ValueError):
    """
    MAGIC stub error raised when a colour string can't be parsed.

    Downstream code usually just treats this like a ValueError, so we
    keep it very simple.
    """


# Small named-colour table for convenience + compatibility.
NAMED_COLOURS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "magenta": (255, 0, 255),
    "cyan": (0, 255, 255),
    "grey": (128, 128, 128),
    "gray": (128, 128, 128),
}


@dataclass(frozen=True)
class Color:
    """
    Minimal RGB colour representation.

    We keep this deliberately small:
    - store as 0–255 integers
    - provide a simple factory and accessor
    """

    red: int
    green: int
    blue: int

    def __post_init__(self) -> None:
        # Clamp to [0, 255] to avoid surprises
        object.__setattr__(self, "red", max(0, min(255, int(self.red))))
        object.__setattr__(self, "green", max(0, min(255, int(self.green))))
        object.__setattr__(self, "blue", max(0, min(255, int(self.blue))))

    # --- basic helpers -----------------------------------------------------

    @classmethod
    def from_rgb(cls, red: int, green: int, blue: int) -> "Color":
        """Create a Colour from integer RGB components."""
        return cls(red=red, green=green, blue=blue)

    @classmethod
    def parse(cls, value: Union[str, Iterable[int], "Color"]) -> "Color":
        """
        Very small parser used as a compatibility shim.

        Accepts:
        - a Color instance  -> returned as-is
        - an iterable of three ints (r, g, b)
        - a hex string like "#RRGGBB" or "RRGGBB"
        - a small set of named colours like "white", "black", etc.

        Anything else raises ColorParseError.
        """
        if isinstance(value, Color):
            return value

        # Tuple / list of three ints
        try:
            if not isinstance(value, str):
                r, g, b = value  # type: ignore[misc]
                return cls(int(r), int(g), int(b))
        except Exception:
            pass

        # Strings
        if isinstance(value, str):
            v = value.strip()
            lower = v.lower()

            # Named colours like "white"
            if lower in NAMED_COLOURS:
                r, g, b = NAMED_COLOURS[lower]
                return cls(r, g, b)

            # Hex strings
            if v.startswith("#"):
                v = v[1:]
            if len(v) == 6:
                try:
                    r = int(v[0:2], 16)
                    g = int(v[2:4], 16)
                    b = int(v[4:6], 16)
                    return cls(r, g, b)
                except Exception as exc:  # pragma: no cover - defensive
                    raise ColorParseError(f"Invalid hex colour: {value!r}") from exc

        raise ColorParseError(f"Cannot parse colour value: {value!r}")

    def get_truecolor(self) -> Tuple[int, int, int]:
        """Return (r, g, b) tuple."""
        return self.red, self.green, self.blue

    def __iter__(self):
        # Allows tuple(Color(...))
        yield self.red
        yield self.green
        yield self.blue


class ColorSystem(str, Enum):
    """
    MAGIC stub for terminal colour systems.

    Only the names need to exist for downstream code; the exact values
    are not critical.
    """

    STANDARD = "standard"      # 16-colour basic terminal palette
    EIGHT_BIT = "eight_bit"    # 256-colour mode
    TRUECOLOR = "truecolor"    # 24-bit RGB


def _clamp_channel(value: float) -> int:
    """Clamp a floating-point channel to 0–255 and return an int."""
    return max(0, min(255, int(round(value))))


def blend_rgb(
    color1: Union[Color, Tuple[int, int, int]],
    color2: Union[Color, Tuple[int, int, int]],
    alpha: float = 0.5,
) -> Tuple[int, int, int]:
    """
    MAGIC stub for blending two RGB colours.

    Parameters
    ----------
    color1, color2:
        Either Color instances or (r, g, b) tuples with 0–255 ints.
    alpha:
        Blend factor between 0.0 and 1.0.
        - 0.0 => 100% color1
        - 1.0 => 100% color2

    Returns
    -------
    (r, g, b) tuple (ints in 0–255).

    If anything goes wrong, we fall back to color1's RGB tuple.
    """
    try:
        c1 = Color.parse(color1)  # type: ignore[arg-type]
        c2 = Color.parse(color2)  # type: ignore[arg-type]

        a = float(alpha)
        if a < 0.0:
            a = 0.0
        if a > 1.0:
            a = 1.0

        r = _clamp_channel(c1.red + (c2.red - c1.red) * a)
        g = _clamp_channel(c1.green + (c2.green - c1.green) * a)
        b = _clamp_channel(c1.blue + (c2.blue - c1.blue) * a)
        return r, g, b
    except Exception:
        # Defensive: if parsing failed or anything else went wrong, just
        # return colour 1 in truecolour form.
        if isinstance(color1, Color):
            return color1.get_truecolor()
        try:
            r, g, b = color1  # type: ignore[misc]
            return int(r), int(g), int(b)
        except Exception:
            return 0, 0, 0


__all__ = [
    "Color",
    "ColorParseError",
    "ColorSystem",
    "blend_rgb",
]
