"""Intégration Phase de la Lune."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .frontend import async_register_card

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR]
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Enregistre la carte Lovelace (une seule fois)."""
    hass.data.setdefault(DOMAIN, {})
    if not hass.data[DOMAIN].get("_card_registered"):
        try:
            await async_register_card(hass)
            hass.data[DOMAIN]["_card_registered"] = True
        except Exception as err:  # noqa: BLE001
            _LOGGER.warning("Carte Lovelace non enregistrée : %s", err)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurer depuis une entrée."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_reload))
    return True


async def _reload(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharger une entrée."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
