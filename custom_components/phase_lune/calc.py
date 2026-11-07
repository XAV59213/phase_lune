"""Calcul local de la phase, de l'illumination, du texte poétique et de l'anecdote du jour."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .astro import elongation, illumination
from .const import PHASES, POETICS, SYNODIC_MONTH

ANECDOTES: list[dict[str, Any]] = json.loads(
    (Path(__file__).parent / "anecdotes.json").read_text("utf-8")
)


def moon_age(now: datetime | None = None) -> float:
    """Âge lunaire équivalent en jours (0 → 29.53), dérivé de l'élongation vraie Lune−Soleil."""
    now = now or datetime.now(timezone.utc)
    return elongation(now) / 360.0 * SYNODIC_MONTH


def phase_slug(age: float) -> str:
    """Slug de phase, seuils alignés sur HA core Moon (échelle 0–28)."""
    p = age * 28.0 / SYNODIC_MONTH
    if p < 0.5 or p > 27.5:
        return "new_moon"
    if p < 6.5:
        return "waxing_crescent"
    if p < 7.5:
        return "first_quarter"
    if p < 13.5:
        return "waxing_gibbous"
    if p < 14.5:
        return "full_moon"
    if p < 20.5:
        return "waning_gibbous"
    if p < 21.5:
        return "last_quarter"
    return "waning_crescent"


def day_of_year_365(d: datetime) -> int:
    """Jour 1–365 lié à la date du calendrier (année non bissextile) : le 29 février
    reprend l'anecdote du 28, et du 1er mars au 31 décembre chaque date garde la même
    anecdote quelle que soit l'année (avant : décalage d'un jour et 30/31 déc. identiques)."""
    day = 28 if (d.month, d.day) == (2, 29) else d.day
    return datetime(2001, d.month, day).timetuple().tm_yday


def compute(now: datetime | None = None) -> dict[str, Any]:
    age = moon_age(now)
    slug = phase_slug(age)
    fr, icon, _ = PHASES[slug]
    local = datetime.now().astimezone() if now is None else now
    doy = day_of_year_365(local)
    poems = POETICS[slug]
    poetic, poetic_en = poems[local.toordinal() % len(poems)]
    anec = ANECDOTES[doy - 1]
    illum = illumination(age / SYNODIC_MONTH * 360.0)
    return {"slug": slug, "fr": fr, "icon": icon, "poetic": poetic,
            "poetic_en": poetic_en, "poetics": [p[0] for p in poems],
            "anecdote": anec["fr"], "anecdote_en": anec["en"], "day_of_year": doy,
            "illumination": round(illum, 1), "age_days": round(age, 2)}
