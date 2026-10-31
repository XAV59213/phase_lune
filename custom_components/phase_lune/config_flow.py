"""Config flow pour Phase de la Lune."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig, SelectSelectorMode

from .const import COUNTRIES, CONF_COUNTRY, DEFAULT_COUNTRY, DOMAIN, NAME


def _schema(default: str) -> vol.Schema:
    return vol.Schema({vol.Required(CONF_COUNTRY, default=default): SelectSelector(
        SelectSelectorConfig(options=list(COUNTRIES), mode=SelectSelectorMode.DROPDOWN,
                             translation_key="country"))})


class PhaseLuneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Flux de configuration : choix du pays (défaut France)."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(title=NAME, data=user_input)
        return self.async_show_form(step_id="user", data_schema=_schema(DEFAULT_COUNTRY))

    @staticmethod
    @callback
    def async_get_options_flow(entry):
        return PhaseLuneOptionsFlow()


class PhaseLuneOptionsFlow(config_entries.OptionsFlow):
    """Changer de pays après installation."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        cur = str(self.config_entry.options.get(CONF_COUNTRY, self.config_entry.data.get(CONF_COUNTRY, DEFAULT_COUNTRY))).lower()
        return self.async_show_form(step_id="init", data_schema=_schema(cur))
