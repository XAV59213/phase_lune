"""Capteurs Phase de la Lune (calcul 100 % local)."""
from __future__ import annotations

import json
import math
from pathlib import Path
from datetime import datetime, timedelta, timezone

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import COUNTRIES, CONF_COUNTRY, DEFAULT_COUNTRY, IMAGES_URL, MIRROR, DOMAIN, NAME, PHASES, POETICS, REFERENCE_NEW_MOON_JD, SYNODIC_MONTH, VERSION

SCAN_INTERVAL = timedelta(minutes=15)

ANECDOTES: list[dict] = json.loads(
    (Path(__file__).parent / "anecdotes.json").read_text("utf-8")
)


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
    fr, icon, _ = PHASES[slug]
    local = datetime.now().astimezone() if now is None else now
    doy = min(local.timetuple().tm_yday, 365)
    poems = POETICS[slug]
    poetic, poetic_en = poems[local.toordinal() % len(poems)]
    anec = ANECDOTES[doy - 1]
    illum = (1 - math.cos(2 * math.pi * age / SYNODIC_MONTH)) / 2 * 100
    return {"slug": slug, "fr": fr, "icon": icon, "poetic": poetic,
            "poetic_en": poetic_en, "poetics": [p[0] for p in poems],
            "anecdote": anec["fr"], "anecdote_en": anec["en"], "day_of_year": doy,
            "illumination": round(illum, 1), "age_days": round(age, 2)}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry,
                            async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([MoonPhaseSensor(entry), PhaseDeLaLuneSensor(entry),
                        IlluminationSensor(entry), AnecdoteSensor(entry)], True)


class _BaseMoonSensor(SensorEntity):
    _attr_has_entity_name = False
    _attr_should_poll = True

    def __init__(self, entry: ConfigEntry) -> None:
        self._country = entry.options.get(CONF_COUNTRY, entry.data.get(CONF_COUNTRY, DEFAULT_COUNTRY))
        self._hemi = COUNTRIES.get(self._country, "N")
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

    @property
    def _image_slug(self) -> str:
        slug = self._data["slug"]
        return MIRROR.get(slug, slug) if self._hemi == "S" else slug

    @property
    def entity_picture(self) -> str:
        return f"{IMAGES_URL}/{self._image_slug}.png"

    def _geo(self) -> dict:
        return {"country": self._country, "hemisphere": "south" if self._hemi == "S" else "north",
                "image_slug": self._image_slug}


class MoonPhaseSensor(_BaseMoonSensor):
    """sensor.moon_phase : slug anglais (nom des PNG)."""

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self.entity_id = "sensor.moon_phase"
        self._attr_name = "Phase lunaire (image)"
        self._attr_unique_id = f"{DOMAIN}_moon_phase"

    @property
    def native_value(self) -> str:
        return self._data["slug"]

    @property
    def extra_state_attributes(self) -> dict:
        d = self._data
        return {"illumination": d["illumination"], "age_days": d["age_days"],
                "phase_fr": d["fr"], "poetic": d["poetic"],
                "poetic_en": d["poetic_en"], "poetics": d["poetics"],
                "anecdote": d["anecdote"], "anecdote_en": d["anecdote_en"],
                "day_of_year": d["day_of_year"], **self._geo()}


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
                "phase_slug": d["slug"], "poetic": d["poetic"],
                "poetic_en": d["poetic_en"], "poetics": d["poetics"],
                "anecdote": d["anecdote"], "anecdote_en": d["anecdote_en"],
                "day_of_year": d["day_of_year"], **self._geo()}


class IlluminationSensor(_BaseMoonSensor):
    """sensor.illumination_lune : pourcentage éclairé."""

    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self.entity_id = "sensor.illumination_lune"
        self._attr_name = "Illumination de la Lune"
        self._attr_unique_id = f"{DOMAIN}_illumination"

    @property
    def icon(self) -> str:
        return "mdi:brightness-6"

    @property
    def native_value(self) -> float:
        return self._data["illumination"]

    @property
    def extra_state_attributes(self) -> dict:
        return {"age_days": self._data["age_days"], "phase_slug": self._data["slug"]}


class AnecdoteSensor(_BaseMoonSensor):
    """sensor.anecdote_lune : anecdote du jour (FR), version EN en attribut."""

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self.entity_id = "sensor.anecdote_lune"
        self._attr_name = "Anecdote lunaire du jour"
        self._attr_unique_id = f"{DOMAIN}_anecdote"

    @property
    def icon(self) -> str:
        return "mdi:book-open-variant"

    @property
    def entity_picture(self) -> None:
        return None

    @property
    def native_value(self) -> str:
        return self._data["anecdote"][:255]

    @property
    def extra_state_attributes(self) -> dict:
        d = self._data
        return {"anecdote": d["anecdote"], "anecdote_en": d["anecdote_en"],
                "day_of_year": d["day_of_year"]}
