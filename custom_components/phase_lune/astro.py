"""Position Lune/Soleil basse précision (Jean Meeus, Astronomical Algorithms, 2e éd., ch. 25, 47, 48).

Calcul 100 % local, sans dépendance. Précision de l'élongation ~0,1–0,3° (≈ < 30 min sur
l'instant d'une phase principale), largement suffisante pour un capteur rafraîchi toutes les 15 min.
"""
from __future__ import annotations

import math
from datetime import datetime

# Termes principaux de la longitude lunaire (Meeus table 47.A) : (D, M, M', F, coef 1e-6 deg)
_MOON_LON = (
    (0, 0, 1, 0, 6288774), (2, 0, -1, 0, 1274027), (2, 0, 0, 0, 658314),
    (0, 0, 2, 0, 213618), (0, 1, 0, 0, -185116), (0, 0, 0, 2, -114332),
    (2, 0, -2, 0, 58793), (2, -1, -1, 0, 57066), (2, 0, 1, 0, 53322),
    (2, -1, 0, 0, 45758), (0, 1, -1, 0, -40923), (1, 0, 0, 0, -34720),
    (0, 1, 1, 0, -30383), (2, 0, 0, -2, 15327), (0, 0, 1, 2, -12528),
    (0, 0, 1, -2, 10980), (4, 0, -1, 0, 10675), (0, 0, 3, 0, 10034),
    (4, 0, -2, 0, 8548), (2, 1, -1, 0, -7888), (2, 1, 0, 0, -6766),
    (1, 0, -1, 0, -5163), (1, 1, 0, 0, 4987), (2, -1, 1, 0, 4036),
    (2, 0, 2, 0, 3994), (4, 0, 0, 0, 3861), (2, 0, -3, 0, 3665),
    (0, 1, -2, 0, -2689), (2, 0, -1, 2, -2602), (2, -1, -2, 0, 2390),
    (1, 0, 1, 0, -2348), (2, -2, 0, 0, 2236), (0, 1, 2, 0, -2120),
    (0, 2, 0, 0, -2069), (2, -2, -1, 0, 2048), (2, 0, 1, -2, -1773),
    (2, 0, 0, 2, -1595), (4, -1, -1, 0, 1215), (0, 0, 2, 2, -1110),
)


def _jde(dt: datetime) -> float:
    jd = dt.timestamp() / 86400.0 + 2440587.5
    return jd + 69.2 / 86400.0  # ΔT ≈ 69 s (2020–2030), effet < 1 min ici


def elongation(dt: datetime) -> float:
    """Élongation écliptique Lune − Soleil en degrés [0, 360) : 0 nouvelle, 90 PQ, 180 pleine, 270 DQ."""
    t = (_jde(dt) - 2451545.0) / 36525.0
    r = math.radians
    lp = 218.3164477 + 481267.88123421 * t - 0.0015786 * t * t
    d = 297.8501921 + 445267.1114034 * t - 0.0018819 * t * t
    m = 357.5291092 + 35999.0502909 * t - 0.0001536 * t * t
    mp = 134.9633964 + 477198.8675055 * t + 0.0087414 * t * t
    f = 93.2720950 + 483202.0175233 * t - 0.0036539 * t * t
    e = 1 - 0.002516 * t - 0.0000074 * t * t
    s = 0.0
    for cd, cm, cmp, cf, c in _MOON_LON:
        term = c * math.sin(r(cd * d + cm * m + cmp * mp + cf * f))
        if abs(cm) == 1:
            term *= e
        elif abs(cm) == 2:
            term *= e * e
        s += term
    a1, a2 = 119.75 + 131.849 * t, 53.09 + 479264.290 * t
    s += 3958 * math.sin(r(a1)) + 1962 * math.sin(r(lp - f)) + 318 * math.sin(r(a2))
    moon_lon = lp + s / 1e6
    # Soleil (Meeus ch. 25, basse précision) ; l'aberration/nutation communes s'annulent presque
    l0 = 280.46646 + 36000.76983 * t
    eq = ((1.914602 - 0.004817 * t) * math.sin(r(m)) + 0.019993 * math.sin(r(2 * m))
         + 0.000289 * math.sin(r(3 * m)))
    sun_lon = l0 + eq - 0.00569  # aberration
    return (moon_lon - sun_lon) % 360.0


def illumination(elong: float) -> float:
    """Fraction éclairée en % (Meeus 48.1 avec angle de phase i ≈ 180° − élongation)."""
    return (1 - math.cos(math.radians(elong))) / 2 * 100
