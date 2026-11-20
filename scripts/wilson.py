from math import sqrt
from statistics import NormalDist

CONFIDENCE_LEVEL = 0.90
TARGET_MARGIN_PP = 3
PERCENTAGE_SCALE = 100
MAX_VARIANCE_RATE = 0.5
Z = NormalDist().inv_cdf((1 + CONFIDENCE_LEVEL) / 2)
MARGIN = TARGET_MARGIN_PP / PERCENTAGE_SCALE


def half_width(failures, total):
    if type(total) is not int or type(failures) is not int or not 0 <= failures <= total or total < 1:
        raise ValueError("Require integer 0 <= failures <= total and total > 0")
    return projected_width(failures / total, total)


def projected_width(rate, total):
    if not 0 <= rate <= 1 or total < 1:
        raise ValueError("Invalid forecast")
    variance = rate * (1 - rate)
    return Z * sqrt(variance / total + Z**2 / (4 * total**2)) / (1 + Z**2 / total)


def required_total(rate, margin=MARGIN):
    """Forecast the smallest total with half-width < margin at a fixed rate."""
    if not 0 < margin < 1 or not 0 <= rate <= 1:
        raise ValueError("Invalid rate/margin")
    low, high = 0, 1
    while projected_width(rate, high) >= margin:
        high *= 2
    # Binary-search the first passing total, keeping equality on the failing side.
    while high - low > 1:
        middle = (high + low) // 2
        if projected_width(rate, middle) < margin:
            high = middle
        else:
            low = middle
    return high


WORST_CASE_TOTAL = required_total(MAX_VARIANCE_RATE)
