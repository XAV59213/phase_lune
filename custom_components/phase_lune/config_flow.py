"""Config flow pour Phase de la Lune."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig, SelectSelectorMode

from .const import COUNTRIES, CONF_COUNTRY, DEFAULT_COUNTRY, DOMAIN, NAME


def current_country(entry: ConfigEntry) -> str:
    """Pays effectif : options, sinon data (entrées < 1.3.3), sinon défaut."""
    return str(entry.options.get(CONF_COUNTRY, entry.data.get(CONF_COUNTRY, DEFAULT_COUNTRY))).lower()


def _schema(default: str) -> vol.Schema:
    return vol.Schema({vol.Required(CONF_COUNTRY, default=default): SelectSelector(
        SelectSelectorConfig(options=list(COUNTRIES), mode=SelectSelectorMode.DROPDOWN,
                             translation_key="country"))})


class PhaseLuneConfigFlow(ConfigFlow, domain=DOMAIN):
    """Flux de configuration : choix du pays (défaut France).

    Le pays n'est pas un paramètre de connexion : il est stocké dans ``options``
    (les entrées créées avant 1.3.3 l'ont dans ``data``, toujours lu en repli).
    """

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(title=NAME, data={}, options=user_input)
        return self.async_show_form(step_id="user", data_schema=_schema(DEFAULT_COUNTRY))  # type: ignore[arg-type]  # voluptuous gardé pour HA >= 2024.12

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Reconfigurer le pays sans supprimer l'intégration (entrée existante)."""
        entry = self._get_reconfigure_entry()
        if user_input is not None:
            # data vidée : le pays vit dans options (nettoie les entrées anciennes)
            return self.async_update_reload_and_abort(entry, data={}, options={CONF_COUNTRY: user_input[CONF_COUNTRY]})
        return self.async_show_form(step_id="reconfigure", data_schema=_schema(current_country(entry)))  # type: ignore[arg-type]  # voluptuous gardé pour HA >= 2024.12

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> PhaseLuneOptionsFlow:
        return PhaseLuneOptionsFlow()


class PhaseLuneOptionsFlow(OptionsFlow):
    """Changer de pays après installation."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="init", data_schema=_schema(current_country(self.config_entry)))  # type: ignore[arg-type]  # idem
