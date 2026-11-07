"""Entité de base commune aux capteurs Phase de la Lune."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import Entity

from . import calc
from .const import COUNTRIES, CONF_COUNTRY, DEFAULT_COUNTRY, DOMAIN, IMAGES_URL, MIRROR, NAME, VERSION

_LOGGER = logging.getLogger(__package__)


class PhaseLuneEntity(Entity):
    """Base : appareil de service unique, pays/hémisphère, calcul local."""

    _attr_has_entity_name = True
    _attr_should_poll = True

    def __init__(self, entry: ConfigEntry) -> None:
        self._country = str(entry.options.get(CONF_COUNTRY, entry.data.get(CONF_COUNTRY, DEFAULT_COUNTRY))).lower()
        self._hemi = COUNTRIES.get(self._country, "N")
        self._data: dict[str, Any] = calc.compute()
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=NAME,
            manufacturer="XAV59213",
            model="Calcul local / local computation",
            sw_version=VERSION,
            entry_type=DeviceEntryType.SERVICE,
        )

    def update(self) -> None:
        """Recalcule ; en cas d'erreur inattendue l'entité passe indisponible (journalisé une fois)."""
        try:
            data = calc.compute()
        except Exception as err:  # noqa: BLE001 - toute erreur de calcul/données
            if self._attr_available:
                _LOGGER.info("Phase de la Lune : calcul impossible, entité indisponible (%s)", err)
            self._attr_available = False
            return
        if not self._attr_available:
            _LOGGER.info("Phase de la Lune : calcul rétabli")
        self._attr_available = True
        self._data = data

    @property
    def icon(self) -> str | None:
        return str(self._data["icon"])

    @property
    def _image_slug(self) -> str:
        slug = str(self._data["slug"])
        return MIRROR.get(slug, slug) if self._hemi == "S" else slug

    @property
    def entity_picture(self) -> str | None:
        return f"{IMAGES_URL}/{self._image_slug}.png"

    def _geo(self) -> dict[str, Any]:
        return {"country": self._country, "hemisphere": "south" if self._hemi == "S" else "north",
                "image_slug": self._image_slug}
