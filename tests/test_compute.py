import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from custom_components.phase_lune.const import COUNTRIES, MIRROR, PHASES, POETICS
from custom_components.phase_lune.astro import elongation
from custom_components.phase_lune.sensor import ANECDOTES, compute, day_of_year_365, phase_slug

ROOT = Path(__file__).parent.parent / "custom_components" / "phase_lune"
U = timezone.utc


USNO = json.loads((Path(__file__).parent / "data" / "usno_phases.json").read_text())["phases"]
EVENT = {"New Moon": ("new_moon", 0), "First Quarter": ("first_quarter", 90),
         "Full Moon": ("full_moon", 180), "Last Quarter": ("last_quarter", 270)}


def _dt(p):
    h, m = map(int, p["time"].split(":"))
    return datetime(p["year"], p["month"], p["day"], h, m, tzinfo=U)


def test_usno_reference_dataset_size():
    assert len(USNO) == 249 and {p["year"] for p in USNO} == {2020, 2024, 2025, 2026, 2030}


@pytest.mark.parametrize("p", USNO, ids=lambda p: f"{p['year']}-{p['month']:02}-{p['day']:02}-{p['phase']}")
def test_usno_principal_phases(p):
    """Instants officiels USNO (minute UT) : élongation à ±0,05° (~6 min), catégorie et illumination."""
    slug, target = EVENT[p["phase"]]
    dt = _dt(p)
    err = (elongation(dt) - target + 180) % 360 - 180
    assert abs(err) < 0.05
    d = compute(dt)
    assert d["slug"] == slug
    expected_illum = {0: 0, 90: 50, 180: 100, 270: 50}[target]
    assert abs(d["illumination"] - expected_illum) <= 0.1


@pytest.mark.parametrize("p", [q for q in USNO if q["phase"] in ("First Quarter", "Last Quarter", "Full Moon")][::7],
                         ids=lambda p: f"{p['year']}-{p['month']:02}-{p['day']:02}-{p['phase']}")
def test_transition_window_around_event(p):
    """Convention core HA (échelle 0–28, fenêtre ±0,5) : ±10,7–14,3 h autour de l'instant, voisins au-delà de ±15 h."""
    slug, _ = EVENT[p["phase"]]
    before, after = {"first_quarter": ("waxing_crescent", "waxing_gibbous"),
                     "full_moon": ("waxing_gibbous", "waning_gibbous"),
                     "last_quarter": ("waning_gibbous", "waning_crescent")}[slug]
    dt = _dt(p)
    for h in (-9, 0, 9):  # vitesse d’élongation ~10,8–14,4°/j → demi-fenêtre 6,43° ≈ 10,7–14,3 h
        assert compute(dt + timedelta(hours=h))["slug"] == slug
    assert compute(dt - timedelta(hours=15))["slug"] == before
    assert compute(dt + timedelta(hours=15))["slug"] == after


def test_former_failure_last_quarter_2024_02_02():
    """Régression : avant, cycle moyen → waning_crescent à cet instant (USNO 23:18 UT)."""
    assert compute(datetime(2024, 2, 2, 23, 18, tzinfo=U))["slug"] == "last_quarter"


def test_illumination_monotonic_waxing():
    t0 = datetime(2024, 1, 11, 11, 57, tzinfo=U)
    vals = [compute(t0 + timedelta(hours=h))["illumination"] for h in range(0, 24 * 14, 6)]
    assert vals == sorted(vals)


def test_slug_bounds():
    from custom_components.phase_lune.const import SYNODIC_MONTH as S
    assert phase_slug(0) == "new_moon" and phase_slug(S - 1e-6) == "new_moon"
    seen = {phase_slug(S * i / 1000) for i in range(1000)}
    assert seen == set(PHASES)


def test_illumination_range_and_doy():
    for m in range(1, 13):
        d = compute(datetime(2025, m, 15, tzinfo=U))
        assert 0 <= d["illumination"] <= 100 and 0 <= d["age_days"] < 29.54
    assert compute(datetime(2025, 1, 1, tzinfo=U))["day_of_year"] == 1
    assert compute(datetime(2025, 12, 31, tzinfo=U))["day_of_year"] == 365
    # année bissextile : alignement calendaire, plus de doublon 30/31 décembre
    assert compute(datetime(2024, 12, 30, tzinfo=U))["day_of_year"] == 364
    assert compute(datetime(2024, 12, 31, tzinfo=U))["day_of_year"] == 365
    assert day_of_year_365(datetime(2024, 2, 29)) == day_of_year_365(datetime(2024, 2, 28)) == 59
    assert day_of_year_365(datetime(2024, 3, 1)) == day_of_year_365(datetime(2025, 3, 1)) == 60
    leap = {day_of_year_365(datetime(2024, 1, 1) + timedelta(days=i)) for i in range(366)}
    assert leap == set(range(1, 366))


def test_anecdotes_365_unique_fr_en():
    data = json.loads((ROOT / "anecdotes.json").read_text("utf-8"))
    assert data == ANECDOTES and len(data) == 365
    assert [a["day"] for a in data] == list(range(1, 366))
    for lang in ("fr", "en"):
        texts = [a[lang].strip() for a in data]
        assert all(texts) and len(set(texts)) == 365


def test_images_card_and_poetics():
    for s in PHASES:
        assert (ROOT / "www" / "moon_phases" / f"{s}.png").is_file()
        assert POETICS[s] and all(fr and en for fr, en in POETICS[s])
    assert (ROOT / "frontend" / "phase-lune-card.js").is_file()
    assert all(MIRROR[MIRROR[k]] == k for k in MIRROR)
    assert set(COUNTRIES.values()) <= {"N", "S"} and "fr" in COUNTRIES
    assert all(k == k.lower() for k in COUNTRIES)


def test_translations_cover_countries():
    for f in ("strings.json", "translations/en.json", "translations/fr.json"):
        t = json.loads((ROOT / f).read_text("utf-8"))
        assert set(t["entity"]["sensor"]) == {"slug", "phase", "illumination", "anecdote"}
        opts = t["selector"]["country"]["options"]
        assert set(COUNTRIES) <= set(opts), f
