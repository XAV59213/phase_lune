"""Capteurs Phase de la Lune (calcul 100 % local)."""
from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .calc import ANECDOTES, compute, day_of_year_365, moon_age, phase_slug  # noqa: F401 (API rétro-compatible)
from .const import DOMAIN, PHASES
from .entity import PhaseLuneEntity

SCAN_INTERVAL = timedelta(minutes=15)
# Calcul purement local, sans appareil ni service à ménager : pas de limite.
PARALLEL_UPDATES = 0


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry,
                            async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([MoonPhaseSensor(entry), PhaseDeLaLuneSensor(entry),
                        IlluminationSensor(entry), AnecdoteSensor(entry)], True)


class _BaseMoonSensor(PhaseLuneEntity, SensorEntity):
    """Capteur de base (compatibilité du nom historique)."""


class MoonPhaseSensor(_BaseMoonSensor):
    """slug anglais (nom des PNG)."""

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_translation_key = "slug"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = list(PHASES)
        self._attr_unique_id = f"{DOMAIN}_moon_phase"

    @property
    def native_value(self) -> str:
        return str(self._data["slug"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        d = self._data
        return {"illumination": d["illumination"], "age_days": d["age_days"],
                "phase_fr": d["fr"], "poetic": d["poetic"],
                "poetic_en": d["poetic_en"], "poetics": d["poetics"],
                "anecdote": d["anecdote"], "anecdote_en": d["anecdote_en"],
                "day_of_year": d["day_of_year"], **self._geo()}


class PhaseDeLaLuneSensor(_BaseMoonSensor):
    """libellé FR."""

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_translation_key = "phase"
        self._attr_unique_id = f"{DOMAIN}_phase_de_la_lune"

    @property
    def native_value(self) -> str:
        return str(self._data["fr"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        d = self._data
        return {"illumination": d["illumination"], "age_days": d["age_days"],
                "phase_slug": d["slug"], "poetic": d["poetic"],
                "poetic_en": d["poetic_en"], "poetics": d["poetics"],
                "anecdote": d["anecdote"], "anecdote_en": d["anecdote_en"],
                "day_of_year": d["day_of_year"], **self._geo()}


class IlluminationSensor(_BaseMoonSensor):
    """pourcentage éclairé."""

    _attr_native_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_translation_key = "illumination"
        self._attr_unique_id = f"{DOMAIN}_illumination"

    @property
    def icon(self) -> str | None:
        return "mdi:brightness-6"

    @property
    def native_value(self) -> float:
        return float(self._data["illumination"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"age_days": self._data["age_days"], "phase_slug": self._data["slug"]}


class AnecdoteSensor(_BaseMoonSensor):
    """anecdote du jour (FR), version EN en attribut."""

    def __init__(self, entry: ConfigEntry) -> None:
        super().__init__(entry)
        self._attr_translation_key = "anecdote"
        self._attr_unique_id = f"{DOMAIN}_anecdote"

    @property
    def icon(self) -> str | None:
        return "mdi:book-open-variant"

    @property
    def entity_picture(self) -> str | None:
        return None

    @property
    def native_value(self) -> str:
        return str(self._data["anecdote"])[:255]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        d = self._data
        return {"anecdote": d["anecdote"], "anecdote_en": d["anecdote_en"],
                "day_of_year": d["day_of_year"]}
