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


class PekaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle configuration through the Home Assistant UI."""

    VERSION = 1

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
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=DEFAULT_NAME): selector.TextSelector(),
                    vol.Required(CONF_LOGIN): selector.TextSelector(),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
                    ),
                    vol.Optional(
                        CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL_MINUTES
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=5, max=1440, mode=selector.NumberSelectorMode.BOX
                        )
                    ),
                }
            ),
            errors=errors,
        )