"""Numbers and text for the reader: the formatters the driver, charts, and report share."""
from __future__ import annotations

import html
import math

NA = "n/a"


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def _compact(number: float, decimals: int) -> str | None:
    """Millions and billions for prose; None when the number is below a million."""
    for scale, suffix in ((1e9, "B"), (1e6, "M")):
        if abs(number) >= scale:
            text = f"{number / scale:,.{decimals}f}".rstrip("0").rstrip(".")
            return f"{text}{suffix}"
    return None


def fmt(value, decimals: int = 2, *, compact: bool = False) -> str:
    """Plain number. compact=True writes 1.25M in prose; tables keep the full figure."""
    if value is None:
        return NA
    number = float(value)
    if not math.isfinite(number):
        return NA
    if compact and (short := _compact(number, decimals)):
        return short
    return f"{number:,.0f}" if number.is_integer() else f"{number:,.{decimals}f}"


def money(value, *, compact: bool = False) -> str:
    """Dollar amount. compact=True writes $12.5M in prose; tables keep the full figure."""
    if value is None:
        return NA
    number = float(value)
    if not math.isfinite(number):
        return NA
    sign = "-" if number < 0 else ""
    magnitude = abs(number)
    if compact and (short := _compact(magnitude, 1)):
        return f"{sign}${short}"
    body = f"{magnitude:,.0f}" if magnitude.is_integer() else f"{magnitude:,.2f}"
    return f"{sign}${body}"


def pct(share: float | None) -> str:
    """Share to one decimal place; a non-zero share never reads as 0.0% or 100.0%."""
    if share is None:
        return NA
    if 0 < share < 0.0005:
        return "<0.1%"
    if 0.9995 <= share < 1:
        return ">99.9%"
    return f"{share:.1%}"
