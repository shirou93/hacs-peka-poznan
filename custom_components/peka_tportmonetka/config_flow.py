"""Config flow for the PEKA tPortmonetka integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector

from .api import PekaApiError, async_get_balance
from .const import (
    CONF_LOGIN,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL_MINUTES,
    DOMAIN,
)


def _account_schema(defaults=None):
    """Build the account form shared by the config and options flows."""
    defaults = defaults or {}
    login_field = (
        vol.Required(CONF_LOGIN, default=defaults[CONF_LOGIN])
        if CONF_LOGIN in defaults
        else vol.Required(CONF_LOGIN)
    )
    password_field = (
        vol.Required(CONF_PASSWORD, default=defaults[CONF_PASSWORD])
        if CONF_PASSWORD in defaults
        else vol.Required(CONF_PASSWORD)
    )

    return vol.Schema(
        {
            vol.Required(
                CONF_NAME,
                default=defaults.get(CONF_NAME, DEFAULT_NAME),
            ): selector.TextSelector(),
            login_field: selector.TextSelector(),
            password_field: selector.TextSelector(
                selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
            ),
            vol.Optional(
                CONF_SCAN_INTERVAL,
                default=defaults.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL_MINUTES),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=5, max=1440, mode=selector.NumberSelectorMode.BOX
                )
            ),
        }
    )


class PekaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle configuration through the Home Assistant UI."""

    VERSION = 1

    @staticmethod
    @config_entries.callback
    def async_get_options_flow(config_entry):
        """Return the options flow for an existing account."""
        return PekaOptionsFlow()

    async def async_step_user(self, user_input=None):
        """Handle the initial setup form."""
        errors = {}

        if user_input is not None:
            try:
                await async_get_balance(self.hass, user_input)
            except PekaApiError:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_input[CONF_LOGIN].lower())
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=_account_schema(),
            errors=errors,
        )


class PekaOptionsFlow(config_entries.OptionsFlow):
    """Handle editing an existing PEKA account."""

    async def async_step_init(self, user_input=None):
        """Handle the account edit form."""
        errors = {}
        current = self.config_entry.data

        if user_input is not None:
            try:
                await async_get_balance(self.hass, user_input)
            except PekaApiError:
                errors["base"] = "cannot_connect"
            else:
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    title=user_input[CONF_NAME],
                    data=user_input,
                )
                return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="init",
            data_schema=_account_schema(
                {
                    **current,
                    CONF_NAME: current.get(CONF_NAME, self.config_entry.title),
                    CONF_LOGIN: current.get(CONF_LOGIN, ""),
                    CONF_PASSWORD: current.get(CONF_PASSWORD, ""),
                }
            ),
            errors=errors,
        )