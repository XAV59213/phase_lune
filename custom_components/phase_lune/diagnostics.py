"""Diagnostics Phase de la Lune (aucune donnée personnelle)."""
from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import calc
from .config_flow import current_country
from .const import COUNTRIES, VERSION

# Rien de sensible n'est stocké ; liste défensive si une clé apparaissait un jour.
TO_REDACT = {"latitude", "longitude", "name", "title", "unique_id", "entry_id"}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Pays/hémisphère, version et état du calcul local."""
    country = current_country(entry)
    try:
        d = await hass.async_add_executor_job(calc.compute)
        calculation: dict[str, Any] = {"ok": True, "slug": d["slug"], "illumination": d["illumination"],
                                       "age_days": d["age_days"], "day_of_year": d["day_of_year"]}
    except Exception as err:  # noqa: BLE001
        calculation = {"ok": False, "error": type(err).__name__}
    return {
        "version": VERSION,
        "config_entry_version": entry.version,
        "country": country,
        "hemisphere": "south" if COUNTRIES.get(country, "N") == "S" else "north",
        "country_known": country in COUNTRIES,
        "legacy_country_in_data": "country" in entry.data,
        "options": async_redact_data(dict(entry.options), TO_REDACT),
        "anecdotes": len(calc.ANECDOTES),
        "calculation": calculation,
    }
