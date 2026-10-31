"""Capteurs Phase de la Lune (calcul 100 % local)."""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, NAME, PHASES, REFERENCE_NEW_MOON_JD, SYNODIC_MONTH, VERSION

SCAN_INTERVAL = timedelta(minutes=15)


def moon_age(now: datetime | None = None) -> float:
    """Âge lunaire en jours (0 → 29.53)."""
    now = now or datetime.now(timezone.utc)
    jd = now.timestamp() / 86400.0 + 2440587.5
    return (jd - REFERENCE_NEW_MOON_JD) % SYNODIC_MONTH


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


def compute(now: datetime | None = None) -> dict:
    age = moon_age(now)
    slug = phase_slug(age)
    fr, icon, poetic = PHASES[slug]
    illum = (1 - math.cos(2 * math.pi * age / SYNODIC_MONTH)) / 2 * 100
    return {"slug": slug, "fr": fr, "icon": icon, "poetic": poetic,
            "illumination": round(illum, 1), "age_days": round(age, 2)}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry,
                            async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([MoonPhaseSensor(entry), PhaseDeLaLuneSensor(entry)], True)


class _BaseMoonSensor(SensorEntity):
    _attr_has_entity_name = False
    _attr_should_poll = True

    def __init__(self, entry: ConfigEntry) -> None:
        self._data: dict = compute()
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": NAME, "manufacturer": "XAV59213", "sw_version": VERSION,
        }

    def update(self) -> None:
        self._data = compute()

    @property
    def icon(self) -> str:
        return self._data["icon"]


class MoonPhaseSensor(_BaseMoonSensor):
    """sensor.moon_phase : slug anglais (nom des PNG)."""

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self.entity_id = "sensor.moon_phase"
        self._attr_name = "Moon phase"
        self._attr_unique_id = f"{DOMAIN}_moon_phase"

    @property
    def native_value(self) -> str:
        return self._data["slug"]

    @property
    def extra_state_attributes(self) -> dict:
        d = self._data
        return {"illumination": d["illumination"], "age_days": d["age_days"],
                "phase_fr": d["fr"], "poetic": d["poetic"]}


class PhaseDeLaLuneSensor(_BaseMoonSensor):
    """sensor.phase_de_la_lune : libellé FR."""

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self.entity_id = "sensor.phase_de_la_lune"
        self._attr_name = "Phase de la Lune"
        self._attr_unique_id = f"{DOMAIN}_phase_de_la_lune"

    @property
    def native_value(self) -> str:
        return self._data["fr"]

    @property
    def extra_state_attributes(self) -> dict:
        d = self._data
        return {"illumination": d["illumination"], "age_days": d["age_days"],
                "phase_slug": d["slug"], "poetic": d["poetic"]}
