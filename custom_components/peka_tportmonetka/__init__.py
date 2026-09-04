from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
	"""Set up the PEKA integration."""
	return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
	"""Set up PEKA from a config entry."""
	entry.async_on_unload(entry.add_update_listener(async_reload_entry))
	await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
	return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
	"""Unload a PEKA config entry."""
	return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
	"""Reload the integration after its configuration changes."""
	await hass.config_entries.async_reload(entry.entry_id)